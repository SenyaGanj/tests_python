import urllib.request
import re

# функция принимает три параметра (1 - url, 2 - путь и имя файла, который создастся при скачивании,
# 3 -флаг движка обработки (если True - обрабатываем с помощью lxml, если False - без библиотек))
def GetScriptTag(url, pathName, lib):

    # открываем страницу и забираем всё содержимое
    try:
        f = urllib.request.urlopen(url)
        text = f.read()
    except urllib.error.HTTPError:
        return 'connect error'
    except urllib.error.URLError:
        return 'url error'
    # записываем содержимое
    try:
        f = open(pathName, 'wb')
        f.write(text)
        f.close()
    except IOError:
        return "An IOError has occurred!"

    if lib:
        # обрабатываем данные страницы с библиотекой lxml
        from lxml import html
        # вытаскиваем все теги script и их параметры
        arScripts = html.fromstring(text).xpath('//script')
        for i in range(0, len(arScripts)):
            # забираем содержимое атрибута src
            srcVal = arScripts[i].attrib.get("src")
            # при пустом значении атрибута src забираем содержимое тега
            arScripts[i] = srcVal if srcVal else arScripts[i].text_content()

    else:
        # обрабатываем данные страницы без библиотек
        # забираем содержимое между <script и </script
        arScripts = re.findall(r'<script(.*?)</script', str(text), re.DOTALL)

        for i in range(0, len(arScripts)):
            # ищем подстроку src
            srcPos = arScripts[i].find('src')
            if srcPos == -1:
                # забираем все сожержимое от конца открывающего тего
                arScripts[i] = arScripts[i][arScripts[i].find('>') + 1:]
            else:
                # забираем все сожержимое атрибута src
                arScripts[i] = arScripts[i][srcPos:]
                # убираем ковычки и "\\"
                arDistr = arScripts[i].split(('"' if bool(arScripts[i].find('"') + 1) else "'"))
                arScripts[i] = arDistr[1].replace("\\", "") if (len(arDistr) == 3) else ""


    return arScripts


print(GetScriptTag('http://sen.mcart.ru/test.php', '/home/python_tests/files/index.html', True))