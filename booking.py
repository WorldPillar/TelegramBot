import json
from DataBase import queries
from Logging import logg


class Book:
    def __init__(self):
        self.book = {"id_emp": None, "id_room": None, "day": None, "id_start": None, "id_end": None}

    def __enter__(self):
        self.book = {"id_emp": None, "id_room": None, "day": None, "id_start": None, "id_end": None}
        return self.book

    def __exit__(self, *args, **kwargs):
        del self.book

    def reload(self):
        self.book = {"id_emp": None,"id_room": None,"day": None,"id_start": None,"id_end": None}

    @logg
    def save(self):
        emp = self.book["id_emp"]
        room = self.book["id_room"]
        day = self.book["day"]
        start = self.book["id_start"]
        end = self.book["id_end"]
        queries.add_booking(emp, room, day, start, end)
        return self.book

    def __str__(self):
        return json.dumps(self.book)
