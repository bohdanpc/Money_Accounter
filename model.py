import _pickle
from _datetime import datetime


class Record(object):
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


def initialise(file_name):
    """Returns list of values we've already added"""
    try:
        with open(file_name, 'rb') as f:
            records = _pickle.load(f)
            f.close()
        return records
    except Exception:
        return []


def save_all(records, file_name):
    """Saves list of all values to file"""
    with open(file_name, 'wb') as f:
        _pickle.dump(records, f)
    f.close()


def check_validity_of_date(date):
    """Returns 'True' if date is valid or 'False' otherwise

    >>> check_validity_of_date("12-28-1990")
    False
    >>> check_validity_of_date("-12-12-12")
    False
    >>> check_validity_of_date("12-12-invalid")
    False
    >>> check_validity_of_date("returns false")
    False
    >>> check_validity_of_date("12--12-12")
    False
    >>> check_validity_of_date("30-02-2016")
    False
    >>> check_validity_of_date("42-12-2012")
    False
    >>> check_validity_of_date("31-04-2016")
    False
    >>> check_validity_of_date("29-02-2017")
    False
    >>> check_validity_of_date("10-04-2017")
    True
    >>> check_validity_of_date("29-02-2016")
    True
    """
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
    """check validity of date, length and coefficent input

    >>> check_validity(["12-35-2012", 125, 12])
    False
    >>> check_validity(["12-10-1996", 123, 10.5])
    True
    >>> check_validity(["10-09-2015", "12", 10])
    True
    >>> check_validity(["5-04-2014", 53.2, "152b"])
    False
    """
    if not check_validity_of_date(item[0]):
        return False
    try:
        item[1] = float(item[1])
        item[2] = float(item[2])
        return True
    except:
        return False


def compare_date(first_date, second_date):
    """Returns '0', '1' or '-1' dependent on equality of parameters

    >>> compare_date("12-12-12","12-12-2017")
    -1
    >>> compare_date("12-12-2017","12-12-12")
    1
    >>> compare_date("12-12-2017","12-12-2017")
    0
    """
    first = first_date.split('-')
    second = second_date.split('-')
    first = datetime(int(first[2]), int(first[1]), int(first[0]))
    second = datetime(int(second[2]), int(second[1]), int(second[0]))
    if first < second:
        return -1
    elif first == second:
        return 0
    return 1


def find_by_date(records, date):
    """Returns list of items by date or 'False' otherwise

    >>> l=[Record("12-01-2017",125,3.14), Record("12-03-2017",250,14.20),\
    Record("12-03-2017",456,55.11)]
    >>> result = find_by_date(l,"12-03-2017")
    >>> result[0].length
    250
    >>> result[1].length
    456
    """
    items = []
    for item in records:
        if item.date == date:
            items.append(item)
    return items


def find_by_date_range(records, first_date, second_date):
    """Returns list of items chosen by date in date range or 'False' otherwise

    >>> l=[Record("12-01-2017",125,3.14), Record("12-02-2017",250,14.20),\
     Record("12-03-2017",456,55.11), Record("12-04-2017",887,15), \
     Record("12-05-2017",337,1.08), Record("12-06-2017",225,0.75)]
    >>> result = find_by_date_range(l,"01-03-2017","22-05-2017")
    >>> result[0].length
    456
    >>> result[1].length
    887
    """
    items = []
    for item in records:
        if compare_date(item.date, first_date) == -1 or \
                        compare_date(item.date, second_date) == 1:
            continue
        else:
            items.append(item)
    return items


def get_used_fuel(record):
    """Returns value of used fuel by given record

    >>> get_used_fuel(Record("12-03-2017",200,10))
    20.0
    """
    return (record.coefficient * record.length) / 100


def get_general_length(records):
    """Returns all length we've passed through

    >>> get_general_length([Record("12-03-2017",300,10),\
    Record("12-03-2017",100,20)])
    400
    """
    res = 0
    for item in records:
        res += item.length
    return res


def get_general_fuel_used(records):
    """Returns all fuel we've spent

    >>> get_general_fuel_used([Record("12-03-2017",300,10),\
     Record("12-03-2017",100,20)])
    50.0
    """
    res = 0
    for item in records:
        res += get_used_fuel(item)
    return res
