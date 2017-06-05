import controller

def menu(input_func=input):
    """Shows menu on the screen

    >>> menu(input_func = lambda:1)
    <BLANKLINE>
    ---Record fuel consumption---
    1) Show the whole table
    2) Show general summary
    3) Show table for a certain period
    4) Show summary for a certain period
    5) Show info by date
    6) Add a new trip
    7) Exit
    Make your choice:1

    >>> menu(input_func = lambda:-5)
    <BLANKLINE>
    ---Record fuel consumption---
    1) Show the whole table
    2) Show general summary
    3) Show table for a certain period
    4) Show summary for a certain period
    5) Show info by date
    6) Add a new trip
    7) Exit
    Make your choice:-5

    >>> menu(input_func = lambda:'abc')
    <BLANKLINE>
    ---Record fuel consumption---
    1) Show the whole table
    2) Show general summary
    3) Show table for a certain period
    4) Show summary for a certain period
    5) Show info by date
    6) Add a new trip
    7) Exit
    Make your choice:'abc'
    """
    print("\n---Record fuel consumption---")
    print("1) Show the whole table")
    print("2) Show general summary")
    print("3) Show table for a certain period")
    print("4) Show summary for a certain period")
    print("5) Show info by date")
    print("6) Add a new trip")
    print("7) Exit")
    print("Make your choice:", end="")
    return input_func()


def enter_date(input_func=input):
    """Asked the customer to enter the date

    >>> enter_date(input_func = lambda:"11-02-1586")
    <BLANKLINE>
    Enter the date(dd-mm-yyyy):'11-02-1586'

    >>> enter_date(input_func = lambda:"dd-mm-yyyy")
    <BLANKLINE>
    Enter the date(dd-mm-yyyy):'dd-mm-yyyy'

    >>> enter_date(input_func = lambda:"ddmmyyyy")
    <BLANKLINE>
    Enter the date(dd-mm-yyyy):'ddmmyyyy'
    """
    print("\nEnter the date(dd-mm-yyyy):", end="")
    date = input_func()
    return date


def enter_period(input_func1=input, input_func2=input):
    """Asked the customer to enter the period

    >>> enter_period(input_func1 = lambda:"11-12-1999", \
    input_func2 = lambda:"10-12-1999")
    <BLANKLINE>
    Enter beginning date(dd-mm-yyyy):Enter ending date(dd-mm-yyyy):\
('11-12-1999', '10-12-1999')

    >>> enter_period(input_func1 = lambda:"dd-mm-yyyy", \
    input_func2 = lambda:"dd1-mm1-yyyy1")
    <BLANKLINE>
    Enter beginning date(dd-mm-yyyy):Enter ending date(dd-mm-yyyy):\
('dd-mm-yyyy', 'dd1-mm1-yyyy1')
    """
    print("\nEnter beginning date(dd-mm-yyyy):", end="")
    date_beg = input_func1()
    print("Enter ending date(dd-mm-yyyy):", end="")
    date_end = input_func2()
    return date_beg, date_end


def enter_trip_details(input_func1=input,
                       input_func2=input, input_func3=input):
    """Asked the customer to enter a new trip

    >>> enter_trip_details(input_func1 = lambda:"11-05-2014", \
    input_func2 = lambda: 452, input_func3 = lambda: 38)
    <BLANKLINE>
    Enter the date of your trip(dd-mm-yyyy):Enter the length of your trip:\
Enter the fuel consumption:['11-05-2014', 452, 38]

    >>> enter_trip_details(input_func1 = lambda:"dd-mm-yyyy", \
    input_func2 = lambda: "aaa", input_func3 = lambda: "bb")
    <BLANKLINE>
    Enter the date of your trip(dd-mm-yyyy):Enter the length of your trip:\
Enter the fuel consumption:['dd-mm-yyyy', 'aaa', 'bb']
    """
    print("\nEnter the date of your trip(dd-mm-yyyy):", end="")
    date = input_func1()
    print("Enter the length of your trip:", end="")
    length = input_func2()
    print("Enter the fuel consumption:", end="")
    coefficient = input_func3()
    return [date, float(length), float(coefficient)]


def print_record(record, used_fuel=-1):
    """Print record on the screen

    >>> from model import Record
    >>> record = Record("12-04-1997", 485, 8.6)
    >>> print_record(record)
    12-04-1997|    485.00|              8.60|     41.71|

    >>> from model import Record
    >>> record = Record("05-07-2014", 45, 65)
    >>> print_record(record, 75)
    05-07-2014|     45.00|             65.00|     75.00|
    """
    print('%10s|%10.2f|%18.2f|' % (record.date, record.length,
                                   record.coefficient), end="")
    if used_fuel != -1:
        print('%10.2f|' % used_fuel)
    else:
        print('%10.2f|' % float(record.length * record.coefficient / 100))


def record_names():
    """Print names of table columns

    >>> record_names()
    <BLANKLINE>
          Date|Length(km)|Consumption(100km)| Fuel used|
    """
    print('\n%10s|%10s|%18s|%10s|' % ("Date", "Length(km)",
                                      "Consumption(100km)", "Fuel used"))


def print_summary(length, fuel_used):
    """Print summary info

    >>> print_summary(0, 0)
    <BLANKLINE>
    General length: 0
    Fuel used: 0

    >>> print_summary(158.2, 85)
    <BLANKLINE>
    General length: 158.2
    Fuel used: 85
    """
    print("\nGeneral length:", length)
    print("Fuel used:", fuel_used)


def invalid_value():
    """Print a message about incorrect value

    >>> invalid_value()
    Invalid values entered
    """
    print("Invalid values entered")
