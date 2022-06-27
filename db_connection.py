import psycopg2


class DBConnector:
    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connection = psycopg2.connect(host="localhost",
                                      dbname="TelegramBot",
                                      user="admin",
                                      password="admin1524",
                                      port="5432")
        return self.connection

    def __exit__(self,*args,**kwargs):
        self.connection.close()