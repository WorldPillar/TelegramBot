"""
Create DataBase
Run once before Bot start
"""

import datetime
import psycopg2
from decouple import config


class DBCreator:
    def __init__(self):
        self.connection = psycopg2.connect(host="localhost",
                                           dbname="postgres",
                                           user="postgres",
                                           password=config('DBPassword', default='admin'),
                                           port="5432")
        self.connection.autocommit = True

    def create_db(self):
        cursor = self.connection.cursor()
        query = "DROP database IF EXISTS telebot"
        cursor.execute(query)
        query = "CREATE database telebot"
        cursor.execute(query)
        self.connection.close()

    def connect_to_db(self):
        self.connection = psycopg2.connect(host="localhost",
                                           dbname="telebot",
                                           user="postgres",
                                           password=config('DBPassword', default='admin'),
                                           port="5432")
        self.connection.autocommit = True

    def create_tables(self):
        cursor = self.connection.cursor()
        query = """CREATE TABLE IF NOT EXISTS rooms
                    (
                        id SERIAL PRIMARY KEY,
                        name character varying(60) UNIQUE COLLATE pg_catalog."default",
                        CONSTRAINT rooms_name_notnull CHECK (NOT (name IS NULL OR name = ''))
                    )
                """
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS employees
                    (
                        id SERIAL PRIMARY KEY,
                        chat_id integer NOT NULL UNIQUE,
                        first_name character varying(250) COLLATE pg_catalog."default",
                        last_name character varying(250) COLLATE pg_catalog."default",
                        user_name character varying(250) COLLATE pg_catalog."default",
                        CONSTRAINT employees_name_notnull CHECK (NOT (user_name is NULL OR user_name = ''))
                    )
                """
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS booking_time
                    (
                        id SERIAL PRIMARY KEY,
                        _time time without time zone UNIQUE
                    )
                """
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS booking
                    (
                        id SERIAL PRIMARY KEY,
                        id_emp integer NOT NULL,
                        id_room integer NOT NULL,
                        day date NOT NULL,
                        id_start integer NOT NULL,
                        id_end integer NOT NULL,
                        CONSTRAINT booking_id_emp_fkey FOREIGN KEY (id_emp)
                            REFERENCES employees (chat_id)
                            ON UPDATE CASCADE
                            ON DELETE CASCADE,
                        CONSTRAINT booking_id_room_fkey FOREIGN KEY (id_room)
                            REFERENCES rooms (id)
                            ON DELETE CASCADE,
                        CONSTRAINT booking_id_end_fkey FOREIGN KEY (id_end)
                            REFERENCES booking_time (id)
                            ON DELETE CASCADE,
                        CONSTRAINT booking_id_start_fkey FOREIGN KEY (id_start)
                            REFERENCES booking_time (id)
                            ON DELETE CASCADE
                    )
                """
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS room_availability
                    (
                        id SERIAL PRIMARY KEY,
                        id_room integer NOT NULL,
                        day date NOT NULL,
                        time_booked_count integer,
                        status boolean NOT NULL,
                        CONSTRAINT booking_count_id_room_fkey FOREIGN KEY (id_room)
                            REFERENCES rooms (id)
                            ON DELETE CASCADE
                    )
                """
        cursor.execute(query)

    def create_triggers(self):
        cursor = self.connection.cursor()
        query = """CREATE FUNCTION set_status() RETURNS trigger AS $set_status$
                        BEGIN
                            IF NEW.time_booked_count < ((SELECT count(*) FROM booking_time) - 1) THEN
                                NEW.status = true;
                            ELSE
                                NEW.status = false;
                            END IF;
                            RETURN NEW;
                        END;
                    $set_status$ LANGUAGE plpgsql;
        
                    CREATE TRIGGER set_status
                        BEFORE INSERT OR UPDATE ON room_availability
                    FOR EACH ROW EXECUTE FUNCTION set_status();
                """
        cursor.execute(query)

        query = """CREATE FUNCTION check_time_interval() RETURNS trigger AS $check_time_interval$
                        BEGIN
                            IF
                                (SELECT count(*) FROM booking
                                    WHERE id_room = NEW.id_room AND 
                                    day = NEW.day AND 
                                    ((id_start <= NEW.id_start AND 
                                    id_end > NEW.id_start) OR 
                                    (id_end >= NEW.id_end AND 
                                    id_start < NEW.id_end))
                                ) > 0 THEN
                                raise exception 'This interval (% - %) already taken', NEW.id_start, NEW.id_end;
                            END IF;
                            RETURN NEW;
                        END;
                    $check_time_interval$ LANGUAGE plpgsql;

                    CREATE TRIGGER check_time_interval
                        BEFORE INSERT OR UPDATE ON booking
                    FOR EACH ROW EXECUTE FUNCTION check_time_interval();
                """
        cursor.execute(query)

        query = """CREATE FUNCTION update_time_count() RETURNS trigger AS $update_time_count$
                        BEGIN
                            IF (TG_OP = 'DELETE') THEN
                                UPDATE room_availability
                                    SET time_booked_count = time_booked_count - OLD.id_end + OLD.id_start
                                    WHERE id_room = OLD.id_room
                                    AND day = OLD.day;
                            ELSIF (TG_OP = 'INSERT') THEN
                                IF (SELECT count(*) FROM room_availability WHERE id_room = NEW.id_room) = 0 THEN
                                    INSERT INTO room_availability (id_room, day, time_booked_count) 
                                    VALUES (NEW.id_room, NEW.day, NEW.id_end - NEW.id_start);
                                ELSE
                                    UPDATE room_availability
                                        SET time_booked_count = time_booked_count + NEW.id_end - NEW.id_start
                                    WHERE id_room = NEW.id_room
                                    AND day = NEW.day;
                                END IF;
                            END IF;
                            RETURN NULL;
                        END;
                    $update_time_count$ LANGUAGE plpgsql;

                    CREATE TRIGGER update_time_count
                        AFTER INSERT OR DELETE ON booking
                    FOR EACH ROW EXECUTE FUNCTION update_time_count();
                """
        cursor.execute(query)

    def insert_default_time(self, interval):
        """
        Заполняет таблицу доступного времени в зависимости от данного интервала:
            Parameters:
                interval - числовое значение, предпочтительно
                            оставить интервал со значением, кратным 5
        """
        in_hour = 60 // interval
        cursor = self.connection.cursor()
        for i in range(9 * in_hour + 1):
            date = datetime.time(int(i//in_hour + 9), int(i % in_hour*interval), int(0)).strftime("%H:%M:%S")
            query = "INSERT INTO booking_time(_time) VALUES ("f"'{date}'"");"
            cursor.execute(query)

    def insert_test_values(self, my_id):
        """
        Заполняет таблицу комнат тестовыми значениям;
        Заполняет таблицу персонала одним тестовым значением;
            Parameters:
                my_id - chat_id пользователя телеграм, которому бот отправляет сообщение
        """
        cursor = self.connection.cursor()
        rooms = ['404', '505', '606', 'steklyashka', 'ConfRoom1', 'ConfRoom2']
        for room in rooms:
            query = "INSERT INTO rooms(name) VALUES ("f"'{room}'"");"
            cursor.execute(query)

        employees = {"chat_id": my_id, "first_name": 'Grand', "last_name": 'Lemon', "user_name": 'Limovskii'}
        query = "INSERT INTO employees(chat_id, first_name, last_name, user_name) VALUES (" \
                f"{employees['chat_id']}, " \
                f"'{employees['first_name']}', " \
                f"'{employees['last_name']}', " \
                f"'{employees['user_name']}');"
        cursor.execute(query)

    def __del__(self):
        self.connection.close()


telebot_db = DBCreator()
telebot_db.create_db()
telebot_db.connect_to_db()
telebot_db.create_tables()
telebot_db.create_triggers()
# Запустить, чтобы заполнить список времён
telebot_db.insert_default_time(15)
# Запустить, чтобы заполнить тестовыми значениями
telebot_db.insert_test_values(385011593)
del telebot_db
