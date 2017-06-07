from configparser import ConfigParser
from os.path import exists
from pathlib import Path
import sqlite3
import _pickle
from _datetime import datetime


def get_general_records_length(records):
    res = 0
    for item in records:
        res += item.length
    return res


def get_general_records_fuel_used(records):
    res = 0
    for item in records:
        res += get_used_fuel(item)
    return res


class Record:
    """Class that represents container for length of the way, date and fuel
    coefficient """

    def __init__(self, _date, _length, _coefficient):
        """Class ctor

        >>> rec = Record("12-01-2017",125.50,3.14198)
        >>> [rec.date,rec.length,rec.coefficient]
        ['12-01-2017', 125.5, 3.14198]
        """
        self.date = _date
        self.length = _length
        self.coefficient = _coefficient


class Model:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read("ini")
        self.db_type = self.config["db-selection"]["db"]
        self.file_name = "FUEL_CONSUMPTION"
        self.db_name = "FUEL_CONSUMPTION"

        if self.db_type == "pickle":
            self.file_name += ".pickle"
            with open(self.file_name, 'rb') as f:
                self.records = _pickle.load(f)
        elif self.db_type == "sqlite":
            self.file_name += ".db"

            if not exists(self.file_name):
                Path(self.file_name).touch(mode=0o666)

            self.conn = sqlite3.connect(self.file_name)
            self.cursor = self.conn.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS FUEL_CONSUMPTION "
                      + "(trip_id INTEGER PRIMARY KEY, date DATE, "
                      + "length FLOAT, coef FLOAT);")
            # self.records = c.fetchall()
            self.conn.commit()

            # c.execute("SELECT * FROM FUEL_CONSUMPTION")
            # print(c.fetchall())
            # conn.close()

    def save_all(self):
        """Saves list of all values to file"""
        if self.db_type == 'pickle':
            with open(self.file_name, 'wb') as f:
                _pickle.dump(self.records, f)
        elif self.db_type == 'sqlite':
            self.conn.close()

    def find_by_date(self, date):
        """Returns list of items by date or 'False' otherwise"""
        items = []
        for item in self.records:
            if item.date == date:
                items.append(item)
        return items

    def find_by_date_range(self, first_date, second_date):
        """Returns list of items chosen by date in date range
        or 'False' otherwise"""
        items = []
        for item in self.records:
            if compare_date(item.date, first_date) == -1 or \
               compare_date(item.date, second_date) == 1:
                continue
            else:
                items.append(item)
        return items

    def get_general_length(self):
        """Returns all length we've passed through"""
        get_general_records_length(self.records)

    def get_general_fuel_used(self):
        """Returns all fuel we've spent"""
        get_general_records_fuel_used(self.records)


def check_validity_of_date(date):
    """Returns 'True' if date is valid or 'False' otherwise"""
    tmp = date.split('-')
    try:
        day, month, year = int(tmp[0]), int(tmp[1]), int(tmp[2])
        if month == 2:
            if year % 4 == 0 and day < 30:
                return True
            elif day > 28:
                return False
        elif month > 12 or day > 31 or (month in (4, 6, 9, 11) and day > 30):
            return False
        return True
    except:
        return False


def check_validity(item):
    """check validity of date, length and coefficent input"""
    if not check_validity_of_date(item[0]):
        return False
    try:
        item[1] = float(item[1])
        item[2] = float(item[2])
        return True
    except ValueError:
        return False


def compare_date(first_date, second_date):
    """Returns '0', '1' or '-1' dependent on equality of parameters"""
    first = first_date.split('-')
    second = second_date.split('-')
    first = datetime(int(first[2]), int(first[1]), int(first[0]))
    second = datetime(int(second[2]), int(second[1]), int(second[0]))
    if first < second:
        return -1
    elif first == second:
        return 0
    return 1


def get_used_fuel(record):
    """Returns value of used fuel by given record"""
    return (record.coefficient * record.length) / 100
