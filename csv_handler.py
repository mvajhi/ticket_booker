import csv

FILE_NAME = "./data.csv"


class Csv_handler:
    def __init__(self, file_name="./data.csv"):
        self.__FILE_NAME = file_name
        self.__csv_data = self.get_data()

    def __update_data(self):
        with open(self.__FILE_NAME) as file:
            reader = csv.DictReader(file)
            self.__csv_data = [i for i in reader]

    def get_data(self) -> list:
        self.__update_data()
        return self.__csv_data

    def add_a_person(self, person_data: dict):
        '''
        dict can be have:
            first_name
            last_name
            nid: national identity code
            birthday: yy/mm/dd
            gender: male or female
        '''
        self.__check_not_duplicate(person_data)
        with open(self.__FILE_NAME, "a") as file:
            writer = csv.DictWriter(file, self.__csv_data[0].keys())
            writer.writerow(person_data)

    def edit_person(self, person_data: dict, change_data: dict):
        row_num = self.__find_person_row(person_data)
        if row_num == None:
            raise "Person NOT FOUND"

        new_data = self.__change_row(self.get_data(), row_num, change_data)

        self.__write_data(new_data)

    # TODO add remove func

    def __write_data(self, data: list):
        '''WARNING: this method clear all data in file and write new data'''
        with open(self.__FILE_NAME, "w") as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    def __change_row(self, data: list, row_num: int, change_data: dict):
        for i in change_data.keys():
            data[row_num][i] = change_data[i]
        return data

    def __check_not_duplicate(self, data: dict):
        if self.__find_person_row(data, True) != None:
            raise "duplicate data!!"

    def __find_person_row(self, data: dict, first_just_check_nid=False):
        file_data = self.get_data()
        for i in range(len(file_data)):
            if self.__is_refer_same(file_data[i], data, first_just_check_nid):
                return i
        return None

    def __is_refer_same(self, data1: dict, data2: dict, first_just_check_nid=False):
        if first_just_check_nid and "nid" in data1 and "nid" in data2:
            if data1["nid"] == data2["nid"]:
                return True
        return all(key in data1 and data1[key] == data2[key] for key in data2) or \
            all(key in data2 and data2[key] == data1[key] for key in data1)


def main():
    test = Csv_handler()

    # print(test.get_data())
    # test.add_a_person({"first_name": "علی", "nid": "1123456789"})
    # test.edit_person({"first_name": "علی"}, {"gender": "male"})

    # test.edit_person({"nid": "0123456789"}, {"gender": "male"})

    test.add_a_person({"first_name": "سلطان", "last_name": "غلامی", "nid": "2823456789", "gender" : "male", "birthday" : "86/7/26"})
    print("\n" * 2)
    print(test.get_data())


if __name__ == "__main__":
    main()
