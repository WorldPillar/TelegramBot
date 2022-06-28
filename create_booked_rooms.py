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
    times = dict(queries.get_booking_time())
    rooms = dict(queries.get_rooms())
    employees = dict(queries.get_employees())
    for book in books:
        employ = f"{employees[book[1]]}"
        room = f"{rooms[book[2]]}"
        time = f"{times[book[4]]}-{times[book[5]]}"
        strbooks += f"{employ}: {room}\n{book[3]} {time}\n"
    if strbooks == "":
        strbooks = "Здесь ещё ничего не было"

    return strbooks
