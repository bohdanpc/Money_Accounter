import view
import model as mdl
from model import Record, Model, get_used_fuel, check_validity_of_date


def show_records(records):
    view.record_names()
    for item in records:
        view.print_record(item, get_used_fuel(item))


def show_records_summary(records):
    view.print_summary(mdl.get_general_records_length(records),
                       mdl.get_general_records_fuel_used(records))


class Controler:
    def __init__(self, model):
        self.model = model

    def run(self):
        choice = ''
        while choice != "7":
            choice = str(view.menu(input))
            if choice == "1":
                self.show_all()
            elif choice == "2":
                self.show_summary()
            elif choice == "3":
                self.show_by_period()
            elif choice == "4":
                self.show_summary_period()
            elif choice == "5":
                self.show_by_date()
            elif choice == "6":
                self.add_record()
            elif choice == "7":
                self.model.save_all()

    def show_all(self):
        """show all present records in database"""
        show_records(self.model.records)

    def show_summary(self):
        """show the sum of km's ridden and fuel used"""
        show_records_summary(self.model.records)

    def show_summary_period(self):
        """show the sum of km's ridden and fuel used
           in date period (from - to)"""
        left, right = view.enter_period(input, input)
        if check_validity_of_date(left) and \
           check_validity_of_date(right):
            records_period = self.model.find_by_date_range(left, right)
            show_records_summary(records_period)
        else:
            view.invalid_value()

    def show_by_date(self, input_func=input):
        """show length ridden and fuel used by certain date"""
        date = view.enter_date(input_func)

        if check_validity_of_date(date):
            records_daily = self.model.find_by_date(date)
            show_records(records_daily)
        else:
            view.invalid_value()

    def show_by_period(self):
        """show length ridden and fuel used by certain period (from - to)"""

        left, right = view.enter_period(input, input)
        if check_validity_of_date(left) and \
           check_validity_of_date(right):
            records_period = self.model.find_by_date_range(left, right)
            show_records(records_period)
        else:
            view.invalid_value()

    def add_record(self):
        """add new record to the database"""
        item_list = view.enter_trip_details(input, input, input)
        if mdl.check_validity(item_list):
            self.model.records.append(
                Record(item_list[0], item_list[1], item_list[2]))
        else:
            view.invalid_value()
