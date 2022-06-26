from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import datetime
import messages
import utils
import queries


def creat_booked_list(chat_id = None):
    if chat_id == None:
        #Выводим все брони
        books = queries.get_booking()
    else:
        #Выводим брони этого человека
        books = queries.get_booking_by_employee(chat_id, None)
    #Books selection
    strbooks = ""
    for book in books:
        strbooks = book + "\n"
    if strbooks == "":
        strbooks = "Здесь ещё ничего не было"

    return strbooks
