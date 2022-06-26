import psycopg2
from psycopg2 import Error

def connect():
    try:
        connection = psycopg2.connect(user="admin",
                                      password="admin",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="TelegramBot")
        cursor = connection.cursor()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")