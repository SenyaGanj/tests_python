import os
import re

def parsFileName(path):
    path = path.strip()

    # обходим каталог
    tree = os.walk(path)
    arResult = []

    # записываем все файлы каталога в arResult
    for root, dirs, files in tree:
        for file in files:
            arResult.append(file)

    # объединяем массив в строку, что бы пропустить его через регулярное выражение в функции re.findall
    arResult = ", ".join(arResult)

    # применяем шаблон регулярного выражения
    arResult = re.findall(r'image-(\S+)-\d{8}T\d{6}.tar.gz', arResult)

    return arResult



print(parsFileName("/home/python_tests/catalog/"))