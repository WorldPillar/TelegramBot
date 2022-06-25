def time_selector_changer(_data, _selected):
    data = _data
    if _selected == None:
        data = data[:-1]
    else:
        i = data[0]
        while i != _selected:
            data.pop(0)
            i = data[0]
        data.pop(0)

    room_booked_erase(data)
    user_booked_erase(data)
    return data

def room_booked_erase(_data):
    data = _data
    return data


def user_booked_erase(_data):
    data = _data
    return data