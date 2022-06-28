from DataBase import queries


def time_selector_changer(data, selected, id_room, id_emp, day):
    if selected != None:
        selected = int(selected)
    all_book = queries.get_booking_by_room(id_room, day)
    emp_book = queries.get_booking_by_employee(id_emp, day)
    data = booked_erase(data, selected, all_book)
    data = booked_erase(data, selected, emp_book)

    if selected == None:
        data = data[:-1]
    else:
        del data[0:selected]
    return data


def booked_erase(data, selected, book_list):
    if selected == None:
        for book in book_list:
            i = 0
            for item in data:
                if item[0] == book[4]:
                    del data[i:book[5]-book[4]+i]
                    break
                i+=1
    else:
        for book in book_list:
            if book[4] > selected:
                del data[book[4]:]
                break
    return data