import json
import re

# принимает два параметра: 1 - файл правил в json формате, 2 - словарь с данными об url
def priorityUrl(regulationsFile, structUrl):
    # достаём словарь правил из файла
    try:
        with open(regulationsFile, 'r') as f:
            regulations = json.loads(f.read())
    except IOError:
        return False

    # устанавливаем начальный приоритет
    priority = int(regulations["begin"])

    # отделяем параметры от чистого адреса
    url = structUrl["url"].split("?")

    # разделяем строку через "/", чтобы вычислить последний раздел адреса
    url[0] = url[0].strip().split("/")
    # делим последний разде через ".", и записываем чать, которая шла после ".", если она есть
    endElem = url[0][-1].split(".")
    endElem = "." + endElem[-1].strip().lower() if len(endElem) > 1 else False

    # смтроим, есть ли такое значение в правилах, если есть, забираем баллы
    if endElem:
        endElem = regulations["url"]["end"][endElem] if endElem in regulations["url"]["end"].keys() else False

    # обрабатываем параметры, если они есть
    getElem = False
    if len(url) > 1:
        # разделяем параметры
        url[1] = url[1].strip().split("&")
        for param in url[1]:
            # разделяем на название параметра и на его значение разделителем "="
            param = param.split("=")
            if len(param) > 1:
                # вытаскиваем окончание значения разделителем "."
                param = param[-1].strip().split(".")
                if len(param) > 1:
                    # ищем окончание в правилах и присваиваем баллы
                    if "." + param[1].strip().lower() in regulations["url"]["get"].keys():
                        getElem = regulations["url"]["get"]["." + param[1].strip().lower()]
                        break
    # вычисляем приоритет для параметра и для окончания ссылки
    priority += int(regulations["url"]["get_and_end"]) if endElem and getElem else \
        int(endElem) if endElem else int(getElem) if getElem else 0

    #обрабатываем домен

    domain = url[0][2]
    domain = domain.split(".")

    # пробегаемся по домену и если такой уровень и такое значение есть в правилах, добавляем баллы
    for i in range(-1, -len(domain) - 1, -1):
        i_str = str(abs(i))
        if i_str in regulations["url"]["domain"].keys():
            if domain[i] in regulations["url"]["domain"][i_str].keys():
                priority += int(regulations["url"]["domain"][i_str][domain[i]])

    #обрабатываем info
    for info in structUrl["info"]:
        if info in regulations["info"].keys():
            priority += int(regulations["info"][info][structUrl["info"][info]]) if structUrl["info"][info] in regulations["info"][info].keys() else 0

    return priority




input1 = {
    "info": {
        "as":19574,
        "as_org":"Corporation Service Company",
        "city": "Wilmington",
        "country":"United States",
        "iso":"US",
        "isp": "Corporation Service Company",
        "org": "Corporation Service Company"
    },
     "url": "http://degeuzen.nl/jeygtgv.exe",
}

input2 = {
    "info": {
        "as": 197068,
        "as_org": "HLL LLC",
        "city": "",
        "country": "Russia",
        "iso": "RU",
        "isp": "HLL LLC",
        "org": "HLL LLC"
    },
    "url": "https://download.geo.drweb.com/pub/drweb/windows/katana/1.0/drweb-1.0-katana.exe?download=MSXML3.DLL",
}

print(priorityUrl("/home/python_tests/regulations.json", input1))
print(priorityUrl("/home/python_tests/regulations.json", input2))