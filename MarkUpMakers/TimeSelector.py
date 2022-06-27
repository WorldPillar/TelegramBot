import queries

def time_selector_changer(data, selected, id_room, id_emp, day):
    if selected != None:
        selected = int(selected)
    data = room_booked_erase(data, selected, id_room, day)
    data = user_booked_erase(data, selected, id_emp, day)

    if selected == None:
        data = data[:-1]
    else:
        i = data[0][0]
        while i != selected:
            data.pop(0)
            i = data[0][0]
        data.pop(0)

    return data

def room_booked_erase(data, selected, id, day):
    booked_rooms = queries.get_booking_by_room(id, day)
    if selected == None:
        for book in booked_rooms:
            del data[book[4]:book[5]]
    else:
        for book in booked_rooms:
            if book[4] < selected:
                continue
            else:
                del data[book[4]:-1]
    return data


def user_booked_erase(data, selected, id, day):
    booked_rooms = queries.get_booking_by_employee(id, day)
    if selected == None:
        for book in booked_rooms:
            del data[book[4]:book[5]]
    else:
        for book in booked_rooms:
            if book[4] < selected:
                continue
            else:
                del data[book[4]:-1]
    return data