from DataBase.db_connection import DBConnector


def get_rooms():
    with DBConnector() as connection:
        cursor = connection.cursor()
        query = "SELECT * FROM rooms"
        cursor.execute(query)
        return cursor.fetchall()


def get_employees():
    with DBConnector() as connection:
        cursor = connection.cursor()
        query = "SELECT * FROM employees"
        cursor.execute(query)
        return cursor.fetchall()


def get_employees():
    with DBConnector() as connection:
        cursor = connection.cursor()
        query = "SELECT * FROM employees"
        cursor.execute(query)
        return cursor.fetchall()


def get_unavailable(day):
    with DBConnector() as connection:
        cursor = connection.cursor()
        query = f"SELECT * FROM booking_count " \
                f"WHERE day = '{day}' AND " \
                f"status = false"
        cursor.execute(query)
        return cursor.fetchall()


def get_booking_time():
    with DBConnector() as connection:
        cursor = connection.cursor()
        query = "SELECT * FROM booking_time"
        cursor.execute(query)
        return cursor.fetchall()


def get_booking():
    with DBConnector() as connection:
        cursor = connection.cursor()
        query = f"SELECT * FROM booking"
        cursor.execute(query)
        return cursor.fetchall()


def get_booking_by_room(id_room, day):
    with DBConnector() as connection:
        cursor = connection.cursor()
        query = f"SELECT * FROM booking WHERE " \
                f"id_room = {id_room} AND " \
                f"day = '{day}'"
        cursor.execute(query)
        return cursor.fetchall()


def get_booking_by_employee(id_emp, day):
    with DBConnector() as connection:
        cursor = connection.cursor()
        query = f"SELECT * FROM booking WHERE " \
                f"id_emp = {id_emp} AND " \
                f"day = '{day}'"
        cursor.execute(query)
        return cursor.fetchall()


def get_booking_by_employee(id_emp, day):
    with DBConnector() as connection:
        cursor = connection.cursor()
        cond = f" AND day = '{day}'"
        if day == None:
            cond = ''
        query = f"SELECT * FROM booking WHERE " \
                f"id_emp = {id_emp} " + cond
        cursor.execute(query)
        return cursor.fetchall()


def add_booking(id_emp, id_room, day, id_start, id_end):
    with DBConnector() as connection:
        cursor = connection.cursor()
        query = f"INSERT INTO booking (id_emp, id_room, day, id_start, id_end) VALUES (" \
                f"{id_emp}, " \
                f"{id_room}, " \
                f"'{day}', " \
                f"{id_start}, " \
                f"{id_end})"
        cursor.execute(query)
