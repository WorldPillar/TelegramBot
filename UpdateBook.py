import json
import os
import queries


class Book:
    def __init__(self):
        self.book = {"user_id": None,"room": None,"day": None,"start": None,"end": None}

    def reload(self):
        self.book = {"user_id": None,"room": None,"day": None,"start": None,"end": None}

    def saveBook(self):
        emp = self.book["user_id"]
        room = self.book["room"]
        day = self.book["day"]
        start = self.book["start"]
        end = self.book["end"]
        queries.add_booking(emp, room, day, start, end)
        # if not os.path.exists("./save"):
        #     os.makedirs("./save")
        # file = open('./save/books.txt', 'a+')
        # file.write(json.dumps(self.book) + "\n")
        # file.close()

    def __str__(self):
        return json.dumps(self.book)
