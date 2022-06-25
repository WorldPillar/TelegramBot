#import telegram
from telegram.ext import Updater,CallbackQueryHandler,CommandHandler
from telegram import  ReplyKeyboardRemove,ParseMode

import utils
import messages
import create_booked_rooms

from calendartelegram import telegramcalendar
from roomtelegram import telegramroom
from timestelegram import telegramtimes

TOKEN = "5374150038:AAFIsUjkkrZBFvHf59rU_96HJOwoLK5vJBM"

# Функция, обрабатывающая команду /start
def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=messages.start_message,
        parse_mode=ParseMode.HTML)


def inline_handler(update, context):
    query = update.callback_query
    kind = utils.separate_callback_data(query.data)[0]
    if kind == messages.CALENDAR_CALLBACK:
        inline_calendar_handler(update, context)
    if kind == messages.ROOM_CALLBACK:
        inline_room_handler(update, context)
    if kind == messages.TIMES_CALLBACK:
        inline_times_handler(update, context)


def inline_calendar_handler(update, context):
    selected,date = telegramcalendar.process_calendar_selection(update, context)
    if selected:
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text=messages.calendar_response_message % (date.strftime("%d/%m/%Y")),
                                 reply_markup=telegramroom.create_room())


def inline_room_handler(update, context):
    selected,room = telegramroom.process_room_selection(update, context)
    if selected:
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text=messages.room_response_message % (room),
                                 reply_markup=telegramtimes.create_times())


def inline_times_handler(update, context):
    selected,action,date = telegramtimes.process_times_selection(update, context)
    if selected and action == "StartTIME":
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text=messages.times_response_start_message % (date.strftime("%H:%M")),
                                 reply_markup=telegramtimes.create_times("End"))
    if selected and action == "EndTIME":
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text=messages.times_response_end_message % (date.strftime("%H:%M")),
                                 reply_markup=ReplyKeyboardRemove())


def book_handler(update, context):
    update.message.reply_text(text=messages.reservation_message,
                              reply_markup=telegramcalendar.create_calendar())


def all_books_handler(update, context):
    update.message.reply_text(text=create_booked_rooms.creat_booked_list(),
                              reply_markup=ReplyKeyboardRemove())


def user_books_handler(update, context):
    update.message.reply_text(text=create_booked_rooms.creat_booked_list(update.message.chat_id),
                              reply_markup=ReplyKeyboardRemove())


if TOKEN == "": print("Please write TOKEN into file")
else:
    updater = Updater(TOKEN, use_context=True)
    dp=updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("book", book_handler))
    dp.add_handler(CommandHandler("allbooks", all_books_handler))
    dp.add_handler(CommandHandler("userbooks", user_books_handler))
    # dp.add_handler(CommandHandler("calendar", calendar_handler))
    # dp.add_handler(CommandHandler("room", room_handler))
    # dp.add_handler(CommandHandler("times", times_handler))
    dp.add_handler(CallbackQueryHandler(inline_handler))

    updater.start_polling()
    updater.idle()