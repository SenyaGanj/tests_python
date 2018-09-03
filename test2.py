import os
import re
import datetime


def whoisFunc(name):

    # выполняем команду whois с переданным доменом
    try:
        output = os.popen("whois "+name)
    except OSError:
        return False

    # разбиваем информацию, которую выдал whois на массив через "\n" отступ
    output = str(output.read()).split("\n")
    # словарь результата
    arResult = {}
    # массив в который будет записываться список name server'ов
    arServers = []
    # флаг того, что у нас есть дата создания, изначально равен False
    flagSuccess = False

    for elem in output:
        # т.к. формат вывода информации у whois для разных доменов может быть разный, попадаются домены,
        # в которых перед выводом информации о домене, находится не нужная информация помеченная %
        # нужно исключиим эту информацию поиском %

        #исключим строки где есть "%" и которые совсем пустые
        if elem.find("%", 0) != -1 or elem.strip() == "":
            continue

        # выходим из массива, как доходим до строчки, где написано про последнее обновление
        if elem.lower().find("last update") != -1:
            break

        # разделяем элемент массива на два значения (ключ:значение)
        elem = elem.strip().split(": ")

        # если значение в массиве только одно, пропускаем строку
        if len(elem) <= 1:
            continue

        # приводим ключ к нижнему регистру
        elem[0] = elem[0].strip().lower()

        # ищем в ключе подстроку "creat", т.е дату создания.
        # Именно "creat", т.к. формат вывода ключей у whois для разных доменов может быть разный
        if elem[0].find("creat", 0) != -1:
            # В случае успеха, обрабатываем дату и записываем в словарь arResult
            arResult[elem[0]] = datetime.datetime.strptime(elem[1].strip(), "%Y-%m-%dT%H:%M:%SZ")
            # Устанавливаем флаг присутствия даты = True
            flagSuccess = True

        # ищем в ключе подстроку "server", т.е имя сервера. Исключаем подстроку whois, т.к.
        # в списке, который выдает whois есть ключ Registrar WHOIS Server
        if elem[0].find("server", 0) != -1 and elem[0].find("whois", 0) == -1:
            # В случае успеха, записываем имя в массив серверов
            arServers.append(elem[1].strip())

        # ищем в ключе подстроку "org", т.е список name server'ов.
        if elem[0].find("org", 0) != -1:
            # В случае успеха, записываем имя организации
            arResult[elem[0].strip()] = elem[1].strip()

    # записываем в словарь результатов массив name server'ов если там есть хотябы один сервер
    if len(arServers) > 0:
        arResult["server lists"] = arServers

    # если дата есть, вызвращаем словарь arResult
    if flagSuccess:
        return arResult
    else:
        return False




print(whoisFunc("drweb.com"))
print(" ")
print(whoisFunc("drweb.ru"))
print(" ")
print(whoisFunc("drweb.net"))
print(" ")
print(whoisFunc("drweb.de"))
