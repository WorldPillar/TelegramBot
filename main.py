from telegram.ext import Updater,CallbackQueryHandler,CommandHandler
from telegram import ReplyKeyboardRemove,ParseMode

from booking import Book
import bookedlist
import utils
import messages

from MarkUpMakers import telegramtimes, telegramcalendar, telegramroom, publication

TOKEN = "5374150038:AAFXm4LL2fbEdzJtMpobwRjnQfO10GiSoDc"
NewBook = Book()


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
    if kind == messages.BOOK_CALLBACK:
        inline_book_handler(update, context)


def inline_calendar_handler(update, context):
    selected,date = telegramcalendar.process_calendar_selection(update, context)
    if selected:
        NewBook.book["day"] = date.strftime("%d/%m/%Y")
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text=messages.calendar_response_message % (date.strftime("%d/%m/%Y")),
                                 reply_markup=telegramroom.create_room(date.strftime("%d/%m/%Y")))


def inline_room_handler(update, context):
    selected,room,name = telegramroom.process_room_selection(update, context)
    if selected:
        NewBook.book["id_room"] = int(room)
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text=messages.room_response_message % name,
                                 reply_markup=telegramtimes.create_times(NewBook.book))
    else:
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text="",
                                 reply_markup=ReplyKeyboardRemove())


def inline_times_handler(update, context):
    start,date,time = telegramtimes.process_times_selection(update, context)
    if start:
        NewBook.book["id_start"] = int(date)
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text=messages.times_response_start_message % time,
                                 reply_markup=telegramtimes.create_times(NewBook.book, date))
    elif start == False:
        NewBook.book["id_end"] = int(date)
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text=messages.times_response_end_message % time,
                                 reply_markup=publication.create_public())
    else:
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text="Выберите новую команду",
                                 reply_markup=ReplyKeyboardRemove())


def inline_book_handler(update, context):
    publicate = publication.process_public_selection(update, context)
    if publicate:
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text=f"Ваша запись зарегистрирована: {NewBook}",
                                 reply_markup=ReplyKeyboardRemove())
        NewBook.save()
        telegramroom.add_unavailable_room(NewBook.book["id_room"], NewBook.book["day"])
    else:
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text=f"Вы отменили запись",
                                 reply_markup=ReplyKeyboardRemove())


def book_handler(update, _):
    NewBook.reload()
    NewBook.book["id_emp"] = update.message.chat_id
    update.message.reply_text(text=messages.reservation_message,
                              reply_markup=telegramcalendar.create_calendar())


def all_books_handler(update, _):
    update.message.reply_text(text=bookedlist.creat_booked_list(),
                              reply_markup=ReplyKeyboardRemove())


def user_books_handler(update, _):
    update.message.reply_text(text=bookedlist.creat_booked_list(update.message.chat_id),
                              reply_markup=ReplyKeyboardRemove())


if TOKEN == "": print("Please write TOKEN into file")
else:
    updater = Updater(TOKEN, use_context=True)
    dp=updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("book", book_handler))
    dp.add_handler(CommandHandler("allbooks", all_books_handler))
    dp.add_handler(CommandHandler("mybooks", user_books_handler))
    dp.add_handler(CallbackQueryHandler(inline_handler))

    updater.start_polling()
    updater.idle()