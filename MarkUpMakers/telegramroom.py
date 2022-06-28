from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import messages
from DataBase import queries
import utils


def create_callback_data(action,id_room,room):
    """ Create the callback data associated to each button"""
    return messages.ROOM_CALLBACK + ";" + ";".join([action, str(id_room), str(room)])


def delete_unavailable_rooms(rooms, day):
    unaval = queries.get_unavailable(day)
    for room in rooms:
        for item in unaval:
            if item[1] == room[0]:
                rooms.remove(room)
    return rooms


def create_room(day):
    keyboard = []
    #Room Selection
    #rooms = DBHandler.get_dataset("rooms")
    rooms = queries.get_rooms()
    rooms = delete_unavailable_rooms(rooms, day)
    if len(rooms) == 0:
        keyboard = [[InlineKeyboardButton("Комнат нет. Начать заново", callback_data=create_callback_data("Restart",0,0))]]
    else:
        for room in rooms:
            button = [InlineKeyboardButton(room[1],callback_data=create_callback_data("ROOM",room[0],room[1]))]
            keyboard.append(button)

    return InlineKeyboardMarkup(keyboard)


def process_room_selection(update,context):
    ret_data = (False,None)
    query = update.callback_query
    # print(query)
    (_,action,id_room,name) = utils.separate_callback_data(query.data)
    if action == "IGNORE":
        context.bot.answer_callback_query(callback_query_id= query.id)
    elif action == "ROOM":
        context.bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
            )
        ret_data = True,id_room,name
    elif action == "Restart":
        context.bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
            )
        ret_data = False,0,0
    else:
        context.bot.answer_callback_query(callback_query_id= query.id,text="Something went wrong!")
        # UNKNOWN
    return ret_data


def add_unavailable_room(room, day):
    booking = queries.get_booking_by_room(room, day)
    times = queries.get_booking_time()
    for book in booking:
        del times[book[4]-1:book[5]]
    if len(times) == 0:
        queries.add_unavailable(room, day)
