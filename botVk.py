import vk_api
import smtplib
from vk_api.longpoll import VkLongPoll, VkEventType
from email.mime.text import MIMEText
from vktools import Keyboard, ButtonColor, Text
import pymysql

# Авторизация бота

vk_session = vk_api.VkApi(token="vk1.a.wx5Up_LnkNTq2sUL8FAVFArNhfQ95Nk1n8T-2HiR8u9W9jyiHBGbk7x-V4WqAnAYmi3EdslapxGjITGK01gRK0P4W3pVC9WAWG722yEf7_4AcrrD3dImtQDPKJw9tnd5WyYQg7OqeaMqc8ovcf2suYMLd1QIOufhjOjdeaq9WDIUDLSCareJ6ugNY8aSye4n9QrSBEwg1vT5aK0jdsj7Uw")
session_api = vk_session.get_api()

# Инициализация класса VkLongPoll

longpoll = VkLongPoll(vk_session)

global fio
global fiopa
global dateBirth
global phoneNumber
global email
global time
global date
global directionNumber
global clinicNumber
global directionTime
global regAdress
global reception
global specDoc
global docName
global dateForQuery
datearr = []
global datearrcut
global timearr
global errorInEmail
timearr = []
position = -2
paidOrFree = 0
errorInEmail = 0
# Подключение к БД

def ConnectToSQL(sql):
    host_name = "sql7.freemysqlhosting.net"
    db_name = "sql7626075"
    password = "hCTsQVEaFL"
    username = "sql7626075"

    connection = pymysql.connect(
        host = host_name,
        port = 3306,
        user = username,
        password = password,
        database = db_name,
        cursorclass = pymysql.cursors.DictCursor
    )

    try:
        if sql == f'SELECT Date From `Doctors` WHERE Speciallity = "{specDoc}" AND Employment = 0':
            with connection.cursor() as cursor:
                cursor.execute(sql)
                rowsDate = cursor.fetchall()
                arr = []
                for rowDate in rowsDate:
                    string = str(rowDate)
                    string = string.replace("{'Date': datetime.date(", "").replace(")}", "").replace(',', '').split()
                    string.reverse()
                    k = 0
                    while k < 2:
                        if len(string[k]) == 1:
                            string[k] = "0" + string[k]
                        k += 1
                    datestr = '.'.join(string)
                    copy = 0
                    if len(datearr) == 0:
                        datearr.append(datestr)
                    else:
                        for i in datearr:
                            copy += 1
                            if datestr == i:
                                break
                            elif copy == len(datearr):
                                datearr.append(datestr)
                    del string[2]
                    string = '.'.join(string)
                    copy = 0
                    if len(arr) == 0:
                        arr.append(string)
                    else:
                        for i in arr:
                            copy += 1
                            if string == i:
                                break
                            elif copy == len(arr):
                                arr.append(string)
            return arr
        
        elif sql == f'SELECT Time From `Doctors` WHERE Speciallity = "{specDoc}" AND Date = "{dateForQuery}" AND Employment = 0':
            with connection.cursor() as cursor:
                    cursor.execute(sql)
                    rowsTime = cursor.fetchall()
                    arr = []
                    for rowTime in rowsTime:
                        string = str(rowTime)
                        string = str(int(string.replace("{'Time': datetime.timedelta(seconds=", "").replace(")}", ""))/3600)
                        string = string.replace(".", ":0")
                        copy = 0
                        if len(arr) == 0:
                            arr.append(string)
                        else:
                            for i in arr:
                                copy += 1
                                if string == i:
                                    break
                                elif copy == len(arr):
                                    arr.append(string)
            arr.sort()
            return arr

        elif sql == f'SELECT Name From `Doctors` WHERE Speciallity = "{specDoc}" AND Date = "{dateForQuery}" AND Time = "{time}:00" AND Employment = 0':
            with connection.cursor() as cursor:
                    cursor.execute(sql)
                    rowsDate = cursor.fetchone()
                    string = str(rowsDate)
                    string = string.replace("{'Name': '", "").replace("'}", "")
            return string

        elif sql == f'UPDATE `Doctors` SET Employment = 1 WHERE Speciallity = "{specDoc}" AND Date = "{dateForQuery}" AND Time = "{time}:00"':
            with connection.cursor() as cursor:
                cursor.execute(sql)
                connection.commit()
    finally:
        connection.close()


# Метод отправки сообщения

def send_message(id, text, keyboard=None): 
    post = {
        'user_id': id, 
        'message': text, 
        'random_id': 0}
    if keyboard != None:
        post['keyboard'] = keyboard.add_keyboard()
    vk_session.method('messages.send', post)

# Отправка сообщения на email

def send_email(message):
    sender = "rixweys@gmail.com"
    password = "slbganxklsjyxbxq"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        messageMime = MIMEText(message)
        server.sendmail(sender, sender, messageMime.as_string())
    except Exception as e:
        print(f"{e}")

def send_email_to_pacient(message):
    sender = "rixweys@gmail.com"
    password = "slbganxklsjyxbxq"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    try:
        server.login(sender, password)
        messageMime = MIMEText(message)
        server.sendmail(sender, email, messageMime.as_string())
        return 0
    except Exception as e:
        print(f"{e}")
        return 1

    # Бот, проверяет в бесконечном цикле входящие действия
    # Бот отвечает на строго заданные сообщения

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:

        #Текст сообщения
        msg = event.text.lower()

        #ID страницы пользоваьеля
        user_id = event.user_id

        if msg == "сброс":
            position = -2

            keyboard = Keyboard(
                [
                    [
                        Text("Начать", ButtonColor.POSITIVE)
                    ]
                ],
                one_time=True
            )
            send_message(user_id, "Прогресс сброшен", keyboard)

        if msg == "отмена":
            position = -2

            keyboard = Keyboard(
                    [
                        [
                            Text("1", ButtonColor.PRIMARY),
                            Text("2", ButtonColor.PRIMARY),
                            Text("3", ButtonColor.PRIMARY)
                        ]
                    ],
                    inline= True
            )
            send_message(user_id, "Запись отменена.\nНапишите соответствующую цифру, если хотите записаться на платной основе - 1, запись по ОМС - 2, задать вопрос - 3.", keyboard)

        elif position == -2:
            if msg == "начать":
                position += 1

                #Создание кнопки
                keyboard = Keyboard(
                    [
                        [
                            Text("Да", ButtonColor.POSITIVE),
                            Text("Нет", ButtonColor.NEGATIVE)
                        ]
                    ],
                    inline=True
                )
                send_message(user_id, "Продолжая запись на прием к врачу, Вы соглашаетесь на обработку ваших персональных данных.", keyboard)
            else:
                keyboard = Keyboard(
                    [
                        [
                            Text("Начать", ButtonColor.POSITIVE)
                        ]
                    ],
                    one_time=True
                )   
                send_message(user_id, "Я не понимаю. Дла продолжения напишите «Начать».", keyboard)
        
        elif position == -1:
            if msg == "да":
                position += 1
                keyboard = Keyboard(
                    [
                        [
                            Text("1", ButtonColor.PRIMARY),
                            Text("2", ButtonColor.PRIMARY),
                            Text("3", ButtonColor.PRIMARY)
                        ]
                    ],
                    inline= True
                )
                send_message(user_id, "Напишите соответствующую цифру, если хотите записаться на платной основе - 1, запись по ОМС - 2, задать вопрос - 3.", keyboard)
            elif msg == "нет":
                keyboard = Keyboard(
                    [
                        [
                            Text("Да", ButtonColor.POSITIVE),
                            Text("Нет", ButtonColor.NEGATIVE)
                        ]
                    ],
                    inline= True
                )
                send_message(user_id, "Если вы не согласны на обработку данных, я не смогу продолжить работу с вами. Если вы передумали напишите «Да».", keyboard)
            else:
                keyboard = Keyboard(
                    [
                        [
                            Text("Да", ButtonColor.POSITIVE),
                            Text("Нет", ButtonColor.NEGATIVE)
                        ]
                    ],
                    inline= True
                )
                send_message(user_id, "Я не понимаю. Напишите «Да» или «Нет».", keyboard)

        elif position == -3:
            if msg != None: 
                send_email(msg)
                position = 0

                keyboard = Keyboard(
                    [
                        [
                            Text("1", ButtonColor.PRIMARY),
                            Text("2", ButtonColor.PRIMARY),
                            Text("3", ButtonColor.PRIMARY)
                        ]
                    ],
                    inline=True
                )
                send_message(user_id, "Ждите. Вскоре наш специалист свяжится с вами.\nЕсли хотите записаться на платной основе напишите цифру 1, запись по ОМС - 2, задать вопрос - 3.", keyboard)

        elif position == 0:
            if msg == "1":
                position = 1
                paidOrFree = 1
                send_message(user_id, "Для выбора специалиста напишите цифру данный ему: \n\n1.   Гастроэнтеролог. \n2.   Детский онколог. \n3.   Детский хирург. \n4.   Детская урология-андрология. \n5.   Невролог. \n6.   Нейрохирург. \n7.   Оториноларинголог (ЛОР, эндоскопия носоглотки). \n8.   Офтальмолог. \n9.   Педиатр. \n10.   Травматолог-ортопед \n11.   УЗИ \n12.   Функциональная диагностика (ЭКГ, ЭЭГ, ТКДГ, УЗДГ, ВП) \n13.  Гастроскопия (ЭГДС, ФГДС)")
            
            elif msg == "2":
                position = 1
                paidOrFree = 2
                send_message(user_id, "Для выбора специалиста напишите цифру данный ему: \n\n1.   Гастроэнтеролог. \n2.   Детский онколог. \n3.   Детский хирург. \n4.   Детская урология-андрология. \n5.   Невролог. \n6.   Нейрохирург. \n7.   Оториноларинголог (ЛОР, эндоскопия носоглотки). \n8.   Офтальмолог. \n9.   Педиатр. \n10.   Травматолог-ортопед \n11.   УЗИ \n12.   Функциональная диагностика (ЭКГ, ЭЭГ, ТКДГ, УЗДГ, ВП) \n13.  Гастроскопия (ЭГДС, ФГДС)")

            elif msg == "3":
                position = -3
                send_message(user_id, "Напишите вопрос и для обратной связи свой Email или номер телефона.")
            else:
                keyboard = Keyboard(
                    [
                        [
                            Text("1", ButtonColor.PRIMARY),
                            Text("2", ButtonColor.PRIMARY),
                            Text("3", ButtonColor.PRIMARY)
                        ]
                    ],
                    inline=True
                )
                send_message(user_id, "Я вас не понимаю, напишите цифру от 1 до 3.", keyboard)

        elif position == 1:
            if msg == "1" or msg == "2" or msg == "3" or msg == "4" or msg == "5" or msg == "6" or msg == "7" or msg == "8" or msg == "9" or msg == "10" or msg == "11" or msg == "12" or msg == "13":
                if msg == "1":
                    specDoc = "Гастроэнтеролог"
                elif msg == "2":
                    specDoc = "Детский онколог"
                elif msg == "3":
                    specDoc = "Детский хирург"
                elif msg == "4":
                    specDoc = "Детская урология-андрология"
                elif msg == "5":
                    specDoc = "Невролог"
                elif msg == "6":
                    specDoc = "Нейрохирург"
                elif msg == "7":
                    specDoc = "Оториноларинголог (ЛОР, эндоскопия носоглотки)"
                elif msg == "8":
                    specDoc = "Офтальмолог"
                elif msg == "9":
                    specDoc = "Педиатр"
                elif msg == "10":
                    specDoc = "Травматолог-ортопед"
                elif msg == "11":
                    specDoc = "УЗИ"
                elif msg == "12":
                    specDoc = "Функциональная диагностика (ЭКГ, ЭЭГ, ТКДГ, УЗДГ, ВП)"
                elif msg == "13":
                    specDoc = "Гастроскопия (ЭГДС, ФГДС)"
                position += 1
                sql = f'SELECT Date From `Doctors` WHERE Speciallity = "{specDoc}" AND Employment = 0'
                datearrcut = ConnectToSQL(sql)
                finallystr = ""
                jan = ""
                feb = ""
                mar = ""
                apr = ""
                may = ""
                jun = ""
                jul = ""
                aug = ""
                sep = ""
                oct = ""
                nov = ""
                dec = ""
                for i in datearr:
                    a = i.replace('.',' ').split()
                    dayNot0 = a[0]
                    if dayNot0[0] == "0":
                        a[0] = dayNot0[1]
                    if a[1] == "01":
                        jan = jan + f"\n{a[0]}"
                    elif a[1] == "02":
                        feb = feb + f"\n{a[0]}"
                    elif a[1] == "03":
                        mar = mar + f"\n{a[0]}"
                    elif a[1] == "04":
                        apr = apr + f"\n{a[0]}"
                    elif a[1] == "05":
                        may = may + f"\n{a[0]}"
                    elif a[1] == "06":
                        jun = jun + f"\n{a[0]}"
                    elif a[1] == "07":
                        jul = jul + f"\n{a[0]}"
                    elif a[1] == "08":
                        aug = aug + f"\n{a[0]}"
                    elif a[1] == "09":
                        sep = sep + f"\n{a[0]}"
                    elif a[1] == "10":
                        oct = oct + f"\n{a[0]}"
                    elif a[1] == "11":
                        nov = nov + f"\n{a[0]}"
                    elif a[1] == "12":
                        dec = dec + f"\n{a[0]}"
                if len(dec) != 0:
                    finallystr = finallystr + f"\nДоступные дни в декабре:{dec}"
                if len(jan) != 0:
                    finallystr = finallystr + f"\nДоступные дни в январе:{jan}"
                if len(feb) != 0:
                    finallystr = finallystr + f"\nДоступные дни в феврале:{feb}"
                if len(mar) != 0:
                    finallystr = finallystr + f"\nДоступные дни в марте:{mar}"
                if len(apr) != 0:
                    finallystr = finallystr + f"\nДоступные дни в апреле:{apr}"
                if len(may) != 0:
                    finallystr = finallystr + f"\nДоступные дни в мае:{may}"
                if len(jun) != 0:
                    finallystr = finallystr + f"\nДоступные дни в июне:{jun}"
                if len(jul) != 0:
                    finallystr = finallystr + f"\nДоступные дни в июле:{jul}"
                if len(aug) != 0:
                    finallystr = finallystr + f"\nДоступные дни в августе:{aug}"
                if len(sep) != 0:
                    finallystr = finallystr +  f"\nДоступные дни в сентябре:{sep}"
                if len(oct) != 0:
                    finallystr = finallystr +  f"\nДоступные дни в октябре:{oct}"
                if len(nov) != 0:
                    finallystr = finallystr +  f"\nДоступные дни в ноябре:{nov}"
                send_message(user_id, f"Выберите дату. \n{finallystr}")
            else:
                send_message(user_id, "Я вас не понимаю напишите число от 1 до 13.")

        elif position == 2:
            if len(msg) <= 2 and msg.isdigit(): 
                duplicatearr = datearrcut
                for i in duplicatearr:
                    j = i.replace('.',' ').split()
                    if len(msg) == 1:
                        msg = "0" + msg
                    if j[0] == msg:
                        string = j
                        for k in datearr:
                            truedate = k
                            k = k.replace('.',' ').split()
                            if k[0] == msg:
                                k.reverse()
                                dateForQuery = '-'.join(k)
                                date = truedate
                                sql = f'SELECT Time From `Doctors` WHERE Speciallity = "{specDoc}" AND Date = "{dateForQuery}" AND Employment = 0'
                                arr = ConnectToSQL(sql)
                                timearr = arr
                                position += 1
                                arr = '\n'.join(arr)
                        send_message(user_id, f"Выберите время: \n\n{arr}")
            else:
                send_message(user_id, "Я не понимаю, что вы написали. Пример написания: 12 или 5")

        elif position == 3: 
            if len(msg) == 5:
                i = 0
                while i < len(timearr):
                    if msg == timearr[i]:
                        i += 1
                        position += 1
                        time = msg
                        sql = f'SELECT Name From `Doctors` WHERE Speciallity = "{specDoc}" AND Date = "{dateForQuery}" AND Time = "{time}:00" AND Employment = 0'
                        docName = ConnectToSQL(sql)
                        send_message(user_id, f"Вас будет принимать {docName}.\nВведите фамилию, имя и отчество пациента.")
                        break
                    elif i == len(timearr) - 1:
                        i += 1
                        send_message(user_id, "Я не понимаю. Попробуйте ввести в виде \"15:00\" или ему подобное на необходимое вами время. ")
                    else:
                     i += 1
            else:
                send_message(user_id, "Я не понимаю. Попробуйте ввести в виде \"15:00\" или ему подобное на необходимое вами время. ")

        #     Запись на амбулаторные услуги на платной основе
        
        elif paidOrFree == 1: 
            if position == 4:
                if msg != None:
                    position += 1
                    fio = msg
                    send_message(user_id, "Введите дату рождения.")

            elif position == 5: 
                if msg != None:
                    position += 1
                    dateBirth = msg
                    send_message(user_id, "Введите контактный телефон.")

            elif position == 6: 
                if msg != None:
                    position += 1
                    phoneNumber = msg
                    send_message(user_id, "Введите свой Email.")

            elif position == 7: 
                if msg != None:
                    email = msg
                    keyboard = Keyboard(
                        [
                            [
                            	Text("1", ButtonColor.PRIMARY),
                            	Text("2", ButtonColor.PRIMARY),
                            	Text("3", ButtonColor.PRIMARY)
                            ]
                        ],
                        inline=True
                    )
                    errorOrNot = send_email_to_pacient(f"{fio}, Вы записаны на {date} на {time}. \nПринемающий врач: {docName} \nНомер телефона: {phoneNumber} \nДата рождения: {dateBirth}.")
                    if errorOrNot == 0:
                        position = 0
                        sql = f'UPDATE `Doctors` SET Employment = 1 WHERE Speciallity = "{specDoc}" AND Date = "{dateForQuery}" AND Time = "{time}:00"'
                        ConnectToSQL(sql)
                        send_message(user_id, f"{fio}, Вы записаны на {date} на {time}. \nПринемающий врач:  {docName} \nНомер телефона: {phoneNumber} \nДата рождения: {dateBirth} \nEmail: {email}\nЕсли хотите записаться на платной основе - 1, запись по ОМС - 2, задать вопрос - 3.", keyboard)
                    elif errorOrNot == 1:
                        send_message(user_id, "Попробуйте ввести еще раз.")

# Запись по ОМС

        elif paidOrFree == 2: 
            if position == 4: 
                if msg != None:
                    position += 1
                    fio = msg
                    send_message(user_id, "Введите номер направления.")

            elif position == 5: 
                if msg != None:
                    position += 1
                    directionNumber = msg
                    send_message(user_id, "Введите номер поликлиники.")

            elif position == 6: 
                if msg != None:
                    position += 1
                    clinicNumber = msg
                    send_message(user_id, "Введите дату выдачи направления.")

            elif position == 7: 
                if msg != None:
                    position += 1
                    directionTime = msg
                    send_message(user_id, "Введите фамилию, имя и отчество родителя.")

            elif position == 8: 
                if msg != None:
                    position += 1
                    fiopa = msg
                    send_message(user_id, "Введите дату рождения.")

            elif position == 9: 
                if msg != None:
                    position += 1
                    dateBirth = msg

                    keyboard = Keyboard(
                        [
                            [
                                Text("Первичный прием", ButtonColor.POSITIVE),
                                Text("Повторный прием", ButtonColor.POSITIVE)
                            ]
                        ],
                        inline=True
                    )
                    send_message(user_id, "Введите вид приема.", keyboard)

            elif position == 10: 
                if msg != None:
                    position += 1
                    reception = msg
                    send_message(user_id, "Введите контактный телефон.")

            elif position == 11: 
                if msg != None:
                    position += 1
                    phoneNumber = msg
                    send_message(user_id, "Введите адрес регистрации.")

            elif position == 12: 
                if msg != None:
                    position += 1
                    regAdress = msg
                    send_message(user_id, "Введите свой Email.")

            elif position == 13: 
                if msg != None:
                    email = msg
                    keyboard = Keyboard(
                        [
                            [
                            	Text("1", ButtonColor.PRIMARY),
                            	Text("2", ButtonColor.PRIMARY),
                            	Text("3", ButtonColor.PRIMARY)
                            ]
                        ],
                        inline=True
                    )
                    errorOrNot = send_email_to_pacient(f"{fio}, Вы записаны на {date} на {time}. \nПринемающий врач: {docName} \nНомер телефона: {phoneNumber} \nДата рождения: {dateBirth}.")
                    if errorOrNot == 0:
                        position = 0
                        sql = f'UPDATE `Doctors` SET Employment = 1 WHERE Speciallity = "{specDoc}" AND Date = "{dateForQuery}" AND Time = "{time}:00"'
                        ConnectToSQL(sql)
                        send_message(user_id, f"{fio}, Вы записаны на {date} на {time}. \nПринемающий врач:  {docName} \nНомер телефона: {phoneNumber} \nДата рождения: {dateBirth} \nEmail: {email}\nЕсли хотите записаться на платной основе - 1, запись по ОМС - 2, задать вопрос - 3.", keyboard)
                    elif errorOrNot == 1:
                        send_message(user_id, "Попробуйте ввести еще раз.")