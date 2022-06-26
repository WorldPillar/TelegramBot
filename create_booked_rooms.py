from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import datetime
import messages
import utils


def creat_booked_list(chat_id = None):
    if chat_id == None:
        #Выводим все брони
        books = []
    else:
        #Выводим брони этого человека
        books = []
    #Books selection
    strbooks = "Риyfn"
    for book in books:
        strbooks = book + "\n"

    return strbooks
