import json


# Реализация класса-обработчика txt-файлов
class TxtDataProcessor():
    def __init__(self, datasource):
        self._datasource = datasource
        self._dataset = None
        self.result = None

    def read(self):
        file = open(self._datasource)
        data = json.load(file)
        file.close()
        self._dataset = data

    def run(self):
        self.read()
        self.result = self._dataset

    def print_result(self):
        print(f'Running TXT-file processor!\n', self.result)


rooms_data = TxtDataProcessor("./DataBase/Rooms.json")
times_data = TxtDataProcessor("./DataBase/Times.json")

def get_dataset(dataset):
    if dataset == "rooms":
        rooms_data.run()
        return rooms_data.result[dataset]
    elif dataset == "times":
        times_data.run()
        return times_data.result[dataset]