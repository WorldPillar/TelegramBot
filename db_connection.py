import psycopg2
from psycopg2 import Error


class DBConnector:
    def __init__(self):
        connection = None

    def connect(self):
        try:
            connection = psycopg2.connect(user="admin",
                                          password="admin",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="TelegramBot")
            return connection
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                connection.close()
                print("Соединение с PostgreSQL закрыто")

    def disconnect(self):
        self.connection.close()
