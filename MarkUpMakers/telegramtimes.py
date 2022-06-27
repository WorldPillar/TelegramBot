from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import datetime
import messages
import utils
import queries
import numpy as np
from DataBase import DBHandler
from . import TimeSelector


def create_callback_data(action,hour,minute):
    """ Create the callback data associated to each button"""
    return messages.TIMES_CALLBACK + ";" + ";".join([action, str(hour), str(minute)])


def create_times(book, selected = None):
    keyboard = []
    #Проверка условия выбора начального времени и конечного
    times = queries.get_booking_time()
    times = TimeSelector.time_selector_changer(times, selected, book["room"], book["user_id"], book["day"])
    if selected == None:
        strSelect = "Start"
    else:
        strSelect = "End"
    #Times selection
    rowcol = 0
    for j in range(int(np.ceil(len(times)/4))):
        row = []
        for i in range(4):
            pos = i + rowcol * 4
            if pos >= len(times):
                row.append(
                    InlineKeyboardButton(" ", callback_data=create_callback_data("IGNORE", 0, 0)))
            else:
                (hour,minute) = utils.separate_time_data(times[pos])
                row.append(InlineKeyboardButton(times[pos],callback_data=create_callback_data(strSelect,hour,minute)))
        rowcol = rowcol + 1
        keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def process_times_selection(update,context):
    ret_data = (False,None)
    query = update.callback_query
    # print(query)
    (_,action,hour,minute) = utils.separate_callback_data(query.data)
    if action == "IGNORE":
        context.bot.answer_callback_query(callback_query_id= query.id)
    elif action == "Start":
        context.bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
            )
        ret_data = True,datetime.time(int(hour),int(minute))
    elif action == "End":
        context.bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
            )
        ret_data = False,datetime.time(int(hour),int(minute))
    else:
        context.bot.answer_callback_query(callback_query_id= query.id,text="Something went wrong!")
        # UNKNOWN
    return ret_data