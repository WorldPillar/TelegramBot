import queries

def time_selector_changer(data, selected, id_room, day, id_emp):
    data = room_booked_erase(data, id_room, day)
    data = user_booked_erase(data, id_emp, day)

    if selected == None:
        data = data[:-1]
    else:
        i = data[0]
        while i != selected:
            data.pop(0)
            i = data[0]
        data.pop(0)

    return data

def room_booked_erase(data, selected, id, day):
    booked_rooms = queries.get_booking_by_room(id, day)
    if selected == None:
        for book in booked_rooms:
            del data[book[id_start]:book[id_end]]
    else:
        for book in booked_rooms:
            if book[id_start] < selected:
                continue
            else:
                del data[book[id_start]:-1]
    return data


def user_booked_erase(data, selected, id, day):
    booked_rooms = queries.get_booking_by_employee(id, day)
    if selected == None:
        for book in booked_rooms:
            del data[book[id_start]:book[id_end]]
    else:
        for book in booked_rooms:
            if book[id_start] < selected:
                continue
            else:
                del data[book[id_start]:-1]
    return data