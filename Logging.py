import os


def logg(fn):
    book = fn()
    if not os.path.exists("./Loggs"):
        os.makedirs("./Loggs")
    file = open('./Loggs/logg.txt', 'a+')
    file.write(book + "\n")
    file.close()
