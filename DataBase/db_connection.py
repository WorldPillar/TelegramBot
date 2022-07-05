import psycopg2


class DBConnector:
    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connection = psycopg2.connect(host="localhost",
                                      dbname="TelegramBot",
                                      user="postgres",
                                      password="admin",
                                      port="5432")
        return self.connection

    def __exit__(self,*args,**kwargs):
        self.connection.commit()
        self.connection.close()