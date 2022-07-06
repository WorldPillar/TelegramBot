from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import messages
import utils
from DataBase import queries
from . import timeselector


def create_callback_data(action, id_time, time):
    """ Create the callback data associated to each button"""
    return messages.TIMES_CALLBACK + ";" + ";".join([action, str(id_time), str(time)])


def create_times(book, selected=None):
    keyboard = []
    # Проверка условия выбора начального времени и конечного
    times = queries.get_booking_time()
    times = timeselector.time_selector_changer(times, selected, book["id_room"], book["id_emp"], book["day"])
    if not times:
        keyboard = [
            [InlineKeyboardButton("Времени нет. Начать заново", callback_data=create_callback_data("Restart", 0, 0))]]
    else:
        if selected is None:
            strselect = "Start"
        else:
            strselect = "End"
        # Times selection
        columns = 0
        rows = []
        for time in times:
            if columns % 4 == 0:
                rows.append([])
            date = time[1].strftime("%H:%M")
            rows[columns // 4].append(InlineKeyboardButton
                                      (date, callback_data=create_callback_data(strselect, time[0], time[1])))
            columns += 1
        for i in range((4 - (columns % 4)) % 4):
            rows[columns // 4].append(InlineKeyboardButton
                                      (" ", callback_data=create_callback_data("IGNORE", 0, 0)))
        for row in rows:
            keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def process_times_selection(update, context):
    ret_data = (False, None)
    query = update.callback_query
    # print(query)
    (_, action, id_time, time) = utils.separate_callback_data(query.data)
    if action == "IGNORE":
        context.bot.answer_callback_query(callback_query_id=query.id)
    elif action == "Start":
        context.bot.edit_message_text(text=query.message.text,
                                      chat_id=query.message.chat_id,
                                      message_id=query.message.message_id
                                      )
        ret_data = True, id_time, time
    elif action == "End":
        context.bot.edit_message_text(text=query.message.text,
                                      chat_id=query.message.chat_id,
                                      message_id=query.message.message_id
                                      )
        ret_data = False, id_time, time
    elif action == "Restart":
        context.bot.edit_message_text(text=query.message.text,
                                      chat_id=query.message.chat_id,
                                      message_id=query.message.message_id
                                      )
        ret_data = None, 0, 0
    else:
        context.bot.answer_callback_query(callback_query_id=query.id, text="Something went wrong!")
        # UNKNOWN
    return ret_data
