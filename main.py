from telegram.ext import Updater, CallbackQueryHandler, CommandHandler
from telegram import ReplyKeyboardRemove, ParseMode
from decouple import config

from booking import Book
import bookedlist
import utils
import messages

from MarkUpMakers import telegramtimes, telegramcalendar, telegramroom, publication

TOKEN = config('TOKEN', default='')
NewBook = Book()


# Функция, обрабатывающая команду /start
def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=messages.start_message,
        parse_mode=ParseMode.HTML)


def inline_handler(update, context):
    """
    Обработчик нажатия кнопок.
    Вызывает конкретный обработчик для каждого вида кнопки
    """
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
    """
    Обработчик нажатия на календарь.
    Если было выбрано конкретное число, вызывает создание списка комнат
    """
    selected, date = telegramcalendar.process_calendar_selection(update, context)
    if selected:
        NewBook.book["day"] = date.strftime("%d/%m/%Y")
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text=messages.calendar_response_message % (date.strftime("%d/%m/%Y")),
                                 reply_markup=telegramroom.create_room(date.strftime("%d/%m/%Y")))


def inline_room_handler(update, context):
    """
    Обработчик списка комнат.
    Если была выбрана конкретная комната, вызывает создание списка доступного времени
    Иначе сбрасывает команду.
    """
    selected, room, name = telegramroom.process_room_selection(update, context)
    if selected:
        NewBook.book["id_room"] = int(room)
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text=messages.room_response_message % name,
                                 reply_markup=telegramtimes.create_times(NewBook.book))
    else:
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text="Выберите другой день",
                                 reply_markup=ReplyKeyboardRemove())


def inline_times_handler(update, context):
    """
    Обработчик списка времени.
    Если было выбрано конкретное начальное время, вызывает повторное создание списка для конечного времени
    Если было выбрано конкретное конечное время, вызывает создание списка публикации брони
    Иначе сбрасывает команду
    """
    first_time, date, time = telegramtimes.process_times_selection(update, context)
    if first_time:
        NewBook.book["id_start"] = int(date)
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text=messages.times_response_start_message % time,
                                 reply_markup=telegramtimes.create_times(NewBook.book, int(date)))
    elif not first_time and first_time is not None:
        NewBook.book["id_end"] = int(date)
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text=messages.times_response_end_message % time,
                                 reply_markup=publication.create_public())
    else:
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text="Выберите другой день",
                                 reply_markup=ReplyKeyboardRemove())


def inline_book_handler(update, context):
    """
    Обработчик публикации брони.
    Если выбрана публикация - записывает значение в БД
    Иначе сбрасывает команду
    """
    publicate = publication.process_public_selection(update, context)
    if publicate:
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text=f"Ваша запись зарегистрирована: {NewBook}",
                                 reply_markup=ReplyKeyboardRemove())
        NewBook.save()
    else:
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text=f"Вы отменили запись",
                                 reply_markup=ReplyKeyboardRemove())


def book_handler(update, context):
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


if TOKEN == "":
    print("Please write TOKEN into file")
else:
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.run_async

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("book", book_handler))
    dp.add_handler(CommandHandler("allbooks", all_books_handler))
    dp.add_handler(CommandHandler("mybooks", user_books_handler))
    dp.add_handler(CallbackQueryHandler(inline_handler))

    updater.start_polling()
    updater.idle()
