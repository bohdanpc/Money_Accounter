import controller


def menu(input_func=input):
    """Shows menu on the screen"""
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
    """Asked the customer to enter the date"""
    print("\nEnter the date(dd-mm-yyyy):", end="")
    date = input_func()
    return date


def enter_period(input_func1=input, input_func2=input):
    """Asked the customer to enter the period"""
    print("\nEnter beginning date(dd-mm-yyyy):", end="")
    date_beg = input_func1()
    print("Enter ending date(dd-mm-yyyy):", end="")
    date_end = input_func2()
    return date_beg, date_end


def enter_trip_details(input_func1=input,
                       input_func2=input, input_func3=input):
    """Asked the customer to enter a new trip"""
    print("\nEnter the date of your trip(dd-mm-yyyy):", end="")
    date = input_func1()
    print("Enter the length of your trip:", end="")
    length = input_func2()
    print("Enter the fuel consumption:", end="")
    coefficient = input_func3()
    return [date, float(length), float(coefficient)]


def print_record(record, used_fuel=-1):
    """Print record on the screen"""
    print('%10s|%10.2f|%18.2f|' % (record.date, record.length,
                                   record.coefficient), end="")
    if used_fuel != -1:
        print('%10.2f|' % used_fuel)
    else:
        print('%10.2f|' % float(record.length * record.coefficient / 100))


def record_names():
    """Print names of table columns"""
    print('\n%10s|%10s|%18s|%10s|' % ("Date", "Length(km)",
                                      "Consumption(100km)", "Fuel used"))


def print_summary(length, fuel_used):
    """Print summary info"""
    print("\nGeneral length:", length)
    print("Fuel used:", fuel_used)


def invalid_value():
    """Print a message about incorrect value"""
    print("Invalid values entered")


def print_table_from_sql(table):
    for row in table:
        print("%10s|%10s|%18s|%10s|"%(str(row[1]),  str(row[2]),  str(row[3]), str(row[4])))
