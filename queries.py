import psycopg2
from psycopg2 import Error


def get_rooms():
    try:
        connection = psycopg2.connect(user="admin",
                                      password="admin",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="TelegramBot")
        cursor = connection.cursor()
        query = "SELECT * FROM rooms"
        cursor.execute(query)
        return cursor.fetchall()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


def get_unavailable():
    cursor = connection.cursor()
    query = "SELECT * FROM unavailable"
    cursor.execute(query)
    return cursor.fetchall()


def get_booking_time():
    cursor = connection.cursor()
    query = "SELECT * FROM booking_time"
    cursor.execute(query)
    return cursor.fetchall()


def get_booking(id_room, day):
    cursor = connection.cursor()
    query = "SELECT * FROM booking WHERE " \
            "id_room = " + id_room + " " \
            "day = day '" + day + "' "
    cursor.execute(query)
    return cursor.fetchall()


def get_booking(id_room, id_emp, day):
    cursor = connection.cursor()
    if id_room == None:
        idr = '*'
    else:
        idr = str(id_room)
    if id_emp == None:
        ide = '*'
    else:
        ide = str(id_emp)
    query = "SELECT * FROM booking WHERE " \
            "id_emp = " + ide + ", "\
            "id_room = " + idr + ", " \
            "day = day '" + day + "' "
    cursor.execute(query)
    return cursor.fetchall()


def add_booking(id_emp, id_room, day, id_start, id_end):
    cursor = connection.cursor()
    query = "INSERT INTO booking (id_emp, id_room, day, id_start, id_end) VALUES (" \
            "{}, " \
            "{}, " \
            "{}, " \
            "{}, " \
            "{})".format(id_emp, id_room, day, id_start, id_end)
    cursor.execute(query)


def add_unavailable(id_room, day):
    cursor = connection.cursor()
    query = "INSERT INTO booking (id_room, day) VALUES (" \
            "{}, " \
            "{})".format(id_room, day)
    cursor.execute(query)