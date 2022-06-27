from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import messages
import queries
import utils
from DataBase import DBHandler


def create_callback_data(action,room):
    """ Create the callback data associated to each button"""
    return messages.ROOM_CALLBACK + ";" + ";".join([action, str(room)])


def create_room():
    keyboard = []
    #Room Selection
    #rooms = DBHandler.get_dataset("rooms")
    rooms = queries.get_rooms()
    for room in rooms:
        button = [InlineKeyboardButton(room[1],callback_data=create_callback_data("ROOM",room[0]))]
        keyboard.append(button)

    return InlineKeyboardMarkup(keyboard)


def process_room_selection(update,context):
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
    else:
        context.bot.answer_callback_query(callback_query_id= query.id,text="Something went wrong!")
        # UNKNOWN
    return ret_data
