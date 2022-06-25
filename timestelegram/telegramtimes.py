from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import datetime
import messages
import utils
import numpy as np
from . import Times


def create_callback_data(action,hour,minute):
    """ Create the callback data associated to each button"""
    return messages.TIMES_CALLBACK + ";" + ";".join([action, str(hour), str(minute)])


def create_times(point = "Start"):
    keyboard = []
    #Проверка условия выбора начального времени и конечного
    times_arr = Times.times
    if point == "Start":
        times_arr = times_arr[:-1]
    else:
        times_arr = times_arr[1:]
    #Times selection
    times_arr = np.array(times_arr).reshape(9, 4)
    for line in times_arr:
        row = []
        for time in line:
            (hour,minute) = utils.separate_time_data(time)
            row.append(InlineKeyboardButton(time,callback_data=create_callback_data(f"{point}TIME",hour,minute)))
        keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def process_times_selection(update,context):
    ret_data = (False,None)
    query = update.callback_query
    # print(query)
    (_,action,hour,minute) = utils.separate_callback_data(query.data)
    if action == "IGNORE":
        context.bot.answer_callback_query(callback_query_id= query.id)
    elif action.find("TIME"):
        context.bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
            )
        ret_data = True,action,datetime.time(int(hour),int(minute))
    else:
        context.bot.answer_callback_query(callback_query_id= query.id,text="Something went wrong!")
        # UNKNOWN
    return ret_data