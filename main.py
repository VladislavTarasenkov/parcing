import gspread
gs = gspread.service_account(filename = "C:/Users/json") #вставить путь json file
import datetime
from datetime import date
from dateutil.parser import parse
import os
week_number = datetime.datetime.today().isocalendar()[1]
now2 = datetime.datetime.now().time()
now3 = 14
now4 = now2.hour

today = datetime.date.today()

tom = today + datetime.timedelta(days=1)
tom = str(tom)
today = str(today)


file = gs.open("Перерывы")
worksheet = file.worksheet(str(week_number) + " неделя")



import json
import lxml

import time
all_days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
from bs4 import BeautifulSoup
import requests
text_op = []
from config import login, passwd
def main():
    all_op2 = {}
    while True:
        list_of_lists = worksheet.get_all_values()


        start = time.time()
        s = requests.session()
        #s.headers.update({"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"})
        payload = {
            "formName":  "loginForm",
            "returnUrl":  "",
            "createToken":  "",
            "login" :  login,
            "passwd" : passwd
        }
        r = s.post(, payload) # вставить ссылку

        r = s.get(url="")#вставить ссылку
        # print(r.text)
        #print(r.text)
        soup = BeautifulSoup(r.text, 'lxml').find('tbody').find_all('td')

        l = []
        b = []
        flag1 = 0
        flag2 = 0

        list_line = [
                    "1-я линия (line1q)",
                    "2-я линия (line2q)",
                     "3-я линия (line3q)",
                     "Top (conversionq)",
                     "Топ Партнёры (conversion_partnerq)",
                     "Колцентр Партнёры (partnerq)",
                     'Обзвон (callsq)',
                     'Сборщик Отзывов (opinionq)',
                     'Трешовая очередь (trashq)',
                     'Тестовая очередь (testq)',
                     'Консультанты (consultantq)',
                     'Претензии (claimq)',
                     'Горячая линия (hotlineq)',
                     "Перезвоны (recall)",
                     'Автодозвон (autocall)',
                     'Колцентр DocDoc (callcenter)']
        all_op = {}
        oper = {"Простой": {}, "Пауза не по расписанию": {}, "Время в паузе": {}, "Unavailable SIP": {}, "Отсутствие на линии": {}}
        #print(l)
        for text in soup:
            l.append(text.text)
        for i in range(len(l)):
            if l[i] in list_line:
                flag_l = l[i]
                all_op.setdefault(flag_l, [])
                i += 1
                continue
            all_op[flag_l].append(l[i])
        list_op = []
        for key in all_op:
            #print(key)
            for i in range(0, len(all_op[key]), 8):
                #print(all_op[key][i:i+8])
                l = all_op[key][i:i+8]
                list_op.append(" ".join(l[1].split()))

                #print(l)
                if(l[1] in all_op2):
                    if(all_op2[l[1]]["статус"] in ["not in use", "ringing"] and l[2] in ["not in use", "ringing"]):
                        all_op2[l[1]]["время в статусе"] = time.time() - all_op2[l[1]]['начальное время']
                        current_datetime = time.time()
                        qq = int(all_op2[l[1]]["время в статусе"]) % 60
                        qq2 = int(all_op2[l[1]]["время в статусе"]) // 60
                        if(qq < 10):
                            qq = "0" + str(qq)
                        else:
                            qq = str(qq)
                        if (qq2 < 10):
                            qq2 = "0" + str(qq2)
                        else:
                            qq2 = str(qq2)
                        qq3 = qq2 + ":" + qq

                        #print(current_datetime)
                        if(int(all_op2[l[1]]["время в статусе"]) > 60):
                            oper["Простой"].setdefault(l[1], [l[0][-3:], int(all_op2[l[1]]["время в статусе"]), qq3, key])
                            #print(l[0], l[1], int(all_op2[l[1]]["время в статусе"]), key)
                    elif(all_op2[l[1]]["статус"] == "paused" and l[2] == "paused"):
                        all_op2[l[1]]["время в статусе"] = time.time() - all_op2[l[1]]['начальное время']
                        qq = int(all_op2[l[1]]["время в статусе"]) % 60
                        qq2 = int(all_op2[l[1]]["время в статусе"]) // 60
                        if (qq < 10):
                            qq = "0" + str(qq)
                        else:
                            qq = str(qq)
                        if (qq2 < 10):
                            qq2 = "0" + str(qq2)
                        else:
                            qq2 = str(qq2)
                        qq3 = qq2 + ":" + qq
                        oper["Время в паузе"].setdefault(l[1], [l[0], all_op2[l[1]]["время в статусе"], qq3, key])
                    elif(all_op2[l[1]]["статус"] == "unavailable" and l[2] == "unavailable"):
                        all_op2[l[1]]["время в статусе"] = time.time() - all_op2[l[1]]['начальное время']
                        oper["Unavailable SIP"].setdefault(l[1], [l[0], int(all_op2[l[1]]["время в статусе"]), key])
                    else:
                        all_op2[l[1]] = {"статус": l[2], 'начальное время': time.time(), "время в статусе": 0}
                else:
                    all_op2[l[1]] = {"статус": l[2], 'начальное время':time.time(), "время в статусе": 0}
        #for key in all_op2:
            #print(key, all_op2[key])
            #print(type(all_op2[key]))
        #end = time.time() - start ## собственно время работы программы
        progul_op = []
        status = ["1", ""]
        #print(list_op)
        for i in range(len(list_of_lists)):
            if (list_of_lists[i][1][-4:] == "2023"):
                list_day = str(parse(list_of_lists[i][1]))[:10]
                if(list_day == today):
                    #print(list_of_lists[i])
                    first = i + 3
                    last = len(list_of_lists) - 1
                    now2 = datetime.datetime.now().time()
                    now3 = now2.minute
                    if (int(now3) // 15 == 0):
                        now3 = "00"
                    else:
                        now3 = str((int(now3) // 15) * 15)
                    now4 = now2.hour
                    flag_time = str(int(now4)) + ":" + now3
                    index = list_of_lists[i].index(flag_time)

                    #print(index, "индекс")
        #print(first, last, "это индексы")
        for k in range(first + 1, last):
            #print("мы тут")
            if(list_of_lists[k][1] in all_days):
                break
            elif(list_of_lists[k][index] != ""):
                #print(list_of_lists[k][1], "1121")
                v = datetime.datetime.today()

                if(list_of_lists[k][1] not in list_op):
                    v = datetime.datetime.today()
                    oper["Отсутствие на линии"].setdefault(list_of_lists[k][1], str(v))
            elif(list_of_lists[k][1] in oper["Время в паузе"] and list_of_lists[k][index] in status):
                oper["Пауза не по расписанию"].setdefault(list_of_lists[k][1], oper["Время в паузе"][list_of_lists[k][1]])
            elif(list_of_lists[k][1] in oper["Время в паузе"] and list_of_lists[k][index] == "1"):
                del oper["Время в паузе"][list_of_lists[k][1]]


        #print(all_op, progul_op, "22334", sep="\n")

        #for key, value in oper.items():
            #print(key)
        time_del = []
        if len(oper["Время в паузе"]) > 0:
            for key, value in oper["Время в паузе"].items():
                if(value[1] <= 900):
                    time_del.append(key)
            if len(time_del) > 0:
                for item in time_del:
                    del oper["Время в паузе"][item]
        os.system('cls')
        for key, value in oper.items():
            print(key)
            for j in value:
                print(j, ":", value[j])
            print()



        time.sleep(15)





main()
#print(end) ## вывод времени
#print(type(end))
# статус, начальное время в этом статусе, время в этом статусе
