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
        #data = data[0:selected]
        i = data[0][0]
        while i != selected:
            data.pop(0)
            i = data[0][0]
        data.pop(0)

    return data


def booked_erase(data, selected, book_list):
    if selected == None:
        for book in book_list:
            del data[book[4]-1:book[5]-1]
    else:
        for book in book_list:
            # if book[4] > selected:
            #     del data[book[4]:]
            #     break
            if book[4] < selected:
                continue
            else:
                del data[book[4]:]
                break
    return data
