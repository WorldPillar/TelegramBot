"""
Сохранение записей в логи
"""


import os
import json


def logg(book):
    if not os.path.exists("./Loggs"):
        os.makedirs("./Loggs")
    file = open('./Loggs/logg.txt', 'a+')
    file.write(json.dumps(book) + "\n")
    file.close()
