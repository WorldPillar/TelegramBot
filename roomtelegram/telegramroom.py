from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import messages
import utils
import numpy as np
from . import Room

def create_callback_data(action,room):
    """ Create the callback data associated to each button"""
    return messages.ROOM_CALLBACK + ";" + ";".join([action, str(room)])

def create_room(year=None,month=None):
    keyboard = []
    #Room Selection
    rooms = Room.rooms
    for room in rooms:
        row = []
        row.append(InlineKeyboardButton(room,callback_data=create_callback_data("ROOM",room)))
        keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def process_room_selection(update,context):
    """
    Process the callback_query. This method generates a new calendar if forward or
    backward is pressed. This method should be called inside a CallbackQueryHandler.
    :param telegram.Bot bot: The bot, as provided by the CallbackQueryHandler
    :param telegram.Update update: The update, as provided by the CallbackQueryHandler
    :return: Returns a tuple (Boolean,datetime.datetime), indicating if a date is selected
                and returning the date if so.
    """
    ret_data = (False,None)
    query = update.callback_query
    # print(query)
    (_,action,room) = utils.separate_callback_data(query.data)
    if action == "IGNORE":
        context.bot.answer_callback_query(callback_query_id= query.id)
    elif action == "ROOM":
        context.bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
            )
        ret_data = True,room
    elif action == "PREV-ROOMS":
        context.bot.answer_callback_query(callback_query_id= query.id)
    elif action == "NEXT-ROOMS":
        context.bot.answer_callback_query(callback_query_id=query.id)
    else:
        context.bot.answer_callback_query(callback_query_id= query.id,text="Something went wrong!")
        # UNKNOWN
    return ret_data
