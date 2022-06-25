from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import messages
import utils

def create_callback_data(action):
    """ Create the callback data associated to each button"""
    return messages.BOOK_CALLBACK + ";" + action


def create_public():
    #Times selection
    keyboard = [[InlineKeyboardButton("Забронировать", callback_data=create_callback_data("Publicate"))],
              [InlineKeyboardButton("Отменить", callback_data=create_callback_data("Cancel"))]]

    return InlineKeyboardMarkup(keyboard)

def process_public_selection(update,context):
    ret_data = (None)
    query = update.callback_query
    # print(query)
    (_,action) = utils.separate_callback_data(query.data)
    if action == "IGNORE":
        context.bot.answer_callback_query(callback_query_id= query.id)
    elif action == "Publicate":
        context.bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
            )
        ret_data = True
    elif action == "Cancel":
        context.bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
            )
        ret_data = False
    else:
        context.bot.answer_callback_query(callback_query_id= query.id,text="Something went wrong!")
        # UNKNOWN
    return ret_data