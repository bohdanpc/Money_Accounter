import view
import model
from model import Record


def show_all(records):
    """show all present records in database

    >>> records = [Record("12-12-2012", 253, 172)]
    >>> show_all(records)
    <BLANKLINE>
          Date|Length(km)|Consumption(100km)| Fuel used|
    12-12-2012|    253.00|            172.00|    435.16|
    """
    view.record_names()
    for item in records:
        view.print_record(item, model.get_used_fuel(item))


def show_summary(records):
    """show the sum of km's ridden and fuel used

    >>> show_summary([Record("12-12-2012", 253, 172),\
    Record("20-11-2015", 128, 123)])
    <BLANKLINE>
    General length: 381
    Fuel used: 592.6
    >>> show_summary([])
    <BLANKLINE>
    General length: 0
    Fuel used: 0
    """
    view.print_summary(model.get_general_length(records),
                       model.get_general_fuel_used(records))


def show_summary_period(records, input_func1=input, input_func2=input):
    """show the sum of km's ridden and fuel used
       in date period (from - to)

    >>> show_summary_period([Record("12-12-2012", 253, 172),\
    Record("20-11-2015", 128, 123)], \
    lambda:"12-10-2012", lambda:"25-01-2016")
    <BLANKLINE>
    Enter beginning date(dd-mm-yyyy):Enter ending date(dd-mm-yyyy):
    General length: 381
    Fuel used: 592.6

    >>> show_summary_period([Record("12-12-2012", 253, 172),\
    Record("20-11-2015", 128, 123)], lambda:"12-10-2009", lambda:"25-01-2013")
    <BLANKLINE>
    Enter beginning date(dd-mm-yyyy):Enter ending date(dd-mm-yyyy):
    General length: 253
    Fuel used: 435.16

    >>> show_summary_period([Record("12-12-2012", 253, 172),\
    Record("20-11-2015", 128, 123)], lambda:"12-25-2013", lambda:"25-01-2014")
    <BLANKLINE>
    Enter beginning date(dd-mm-yyyy):Enter ending date(dd-mm-yyyy):\
Invalid values entered
    """
    left, right = view.enter_period(input_func1, input_func2)
    if model.check_validity_of_date(left) and \
            model.check_validity_of_date(right):
        records_period = model.find_by_date_range(records, left, right)
        show_summary(records_period)
    else:
        view.invalid_value()


def show_by_date(records, input_func=input):
    """show length ridden and fuel used by certain date

    >>> show_by_date([Record("12-12-2012", 253, 172),\
    Record("20-11-2015", 128, 123)], lambda:"12-12-2012")
    <BLANKLINE>
    Enter the date(dd-mm-yyyy):
          Date|Length(km)|Consumption(100km)| Fuel used|
    12-12-2012|    253.00|            172.00|    435.16|
    >>> show_by_date([Record("12-12-2012", 253, 172),\
    Record("20-11-2015", 128, 123)], lambda:"32-12-2017")
    <BLANKLINE>
    Enter the date(dd-mm-yyyy):Invalid values entered
    """
    date = view.enter_date(input_func)

    if model.check_validity_of_date(date):
        records_daily = model.find_by_date(records, date)
        show_all(records_daily)
    else:
        view.invalid_value()


def show_by_period(records, input_func1=input, input_func2=input):
    """show length ridden and fuel used by certain period (from - to)

    >>> show_by_period([Record("12-12-2012", 253, 172),\
    Record("20-11-2015", 128, 123)], lambda:"12-10-2012", lambda:"25-01-2016")
    <BLANKLINE>
    Enter beginning date(dd-mm-yyyy):Enter ending date(dd-mm-yyyy):
          Date|Length(km)|Consumption(100km)| Fuel used|
    12-12-2012|    253.00|            172.00|    435.16|
    20-11-2015|    128.00|            123.00|    157.44|

    >>> show_by_period([Record("12-12-2012", 253, 172),\
    Record("20-11-2015", 128, 123)], lambda:"12-10-2012", lambda:"25-01-2014")
    <BLANKLINE>
    Enter beginning date(dd-mm-yyyy):Enter ending date(dd-mm-yyyy):
          Date|Length(km)|Consumption(100km)| Fuel used|
    12-12-2012|    253.00|            172.00|    435.16|

    >>> show_by_period([Record("12-12-2012", 253, 172),\
     Record("20-11-2015", 128, 123)], \
     lambda:"12-10-2012b", lambda:"42-01-2014")
    <BLANKLINE>
    Enter beginning date(dd-mm-yyyy):Enter ending date(dd-mm-yyyy):\
Invalid values entered
    """

    left, right = view.enter_period(input_func1, input_func2)
    if model.check_validity_of_date(left) and \
            model.check_validity_of_date(right):
        records_period = model.find_by_date_range(records, left, right)
        show_all(records_period)
    else:
        view.invalid_value()


def add_record(records, input_func1=input,
               input_func2=input, input_func3=input):
    """add new record to the database

    >>> add_record([Record("12-12-2012", 253, 172)],\
     lambda:"12-12-2013", lambda:234, lambda:218)
    <BLANKLINE>
    Enter the date of your trip(dd-mm-yyyy):\
Enter the length of your trip:Enter the fuel consumption:
    >>> add_record([Record("12-13-2012", 253, 172)],\
    lambda:"31-4-2013", lambda:134, lambda:228)
    <BLANKLINE>
    Enter the date of your trip(dd-mm-yyyy):Enter the length of your trip:\
Enter the fuel consumption:Invalid values entered
    """
    item_list = view.enter_trip_details(input_func1, input_func2, input_func3)
    if model.check_validity(item_list):
        records.append(Record(item_list[0], item_list[1], item_list[2]))
    else:
        view.invalid_value()


def main_func(input_func1=input):
    """show selection menu and wait for the interaction

    >>> main_func(lambda:"7")
    <BLANKLINE>
    ---Record fuel consumption---
    1) Show the whole table
    2) Show general summary
    3) Show table for a certain period
    4) Show summary for a certain period
    5) Show info by date
    6) Add a new trip
    7) Exit
    Make your choice:
    """

    choice = ''
    records = model.initialise("fuel_consumption.pickle")
    while choice != "7":
        choice = str(view.menu(input_func1))
        if choice == "1":
            show_all(records)
        elif choice == "2":
            show_summary(records)
        elif choice == "3":
            show_by_period(records)
        elif choice == "4":
            show_summary_period(records)
        elif choice == "5":
            show_by_date(records)
        elif choice == "6":
            add_record(records)
        elif choice == "7":
            model.save_all(records, "fuel_consumption.pickle")


main_func()
