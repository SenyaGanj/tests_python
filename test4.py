import re

# функция принимает имя лога и событие, которое нужно отслеживать
def parsLog(log, event):

    try:
        # результирующий массив структур
        arResult = []
        # словарь, который будет заполняться и обнуляться при каждом новом появлении события
        objStruct = {}
        with open(log, 'r') as data_source:
            for row in data_source:
                row = str(row)
                # если словарь пуст, мы ищим событие, если не пуст, собираем поле SF_TEXT с помощью PID
                if objStruct == {}:
                    if row.find(event) != -1:
                        # собираем в словарь PID, SF_AT и задаём SF_TEXT для дальнейшего заполнения
                        objStruct["PID"] = re.findall(r'F-(\d+):', str(row))[0]
                        objStruct["SF_AT"] = re.findall(r'' + event + ' at (\d+)', str(row))[0]
                        objStruct["SF_TEXT"] = ""
                else:
                    if row.find("F-" + objStruct["PID"]) != -1:
                        # с помощью PID собираем поле SF_TEXT из каждой строки массива
                        objStruct["SF_TEXT"] += re.findall(r'Dump: (.+)', str(row))[0] + " \n "
                    else:
                        # если PID не найден => событие закончилось, добавляем словарь в массив
                        arResult.append(objStruct)
                        # обнуляем словарь для поиска следующего события
                        objStruct = {}
        return arResult

    except IOError:
        return "An IOError has occurred!"


print(parsLog("/home/python_tests/log.txt", "Segmentation fault"))