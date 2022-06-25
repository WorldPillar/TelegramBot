def room_handler(update, context):
    update.message.reply_text(text=messages.room_message,
                              reply_markup=telegramroom.create_room())


def times_handler(update, context):
    update.message.reply_text(text=messages.room_message,
                              reply_markup=telegramtimes.create_times(update.message.text))


def calendar_handler(update, context):
    update.message.reply_text(text=messages.calendar_message,
                              reply_markup=telegramcalendar.create_calendar())