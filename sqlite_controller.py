import sqlite3
import model as mdl
import view
import _datetime as dt
from controller import Controler

class SQLiteController:
    def __init__(self, model):
        self.model = model

    def run(self):
        Controler.run(self)

    def show_all(self):
        """show all present records in database"""
        self.model.cursor.execute('SELECT * FROM {}'.format(self.model.db_name))
        table = self.model.cursor.fetchall()
        view.record_names()
        if len(table) > 0:
            for t in table:
                print(str(t[1]) + "\t\t" + str(t[2]) + "\t\t" + str(t[3]) + "\t\t\t\t" +
                      str(t[2] * t[3] / 100))

    def show_summary(self):
        """show the sum of km's ridden and fuel used"""
        self.model.cursor.execute("SELECT SUM(length) FROM {}".format(self.model.db_name))
        length = self.model.cursor.fetchone()[0]
        self.model.cursor.execute("SELECT SUM(coef) FROM {}".format(self.model.db_name))
        coef = self.model.cursor.fetchone()[0]
        cons = length * coef / 100
        print("\nTotal length: " + str(length) +
              "\nTotal consumption: " + str(coef) +
              "\nTotal fuel used: " + str(cons))

    def show_summary_period(self):
        """show the sum of km's ridden and fuel used
           in date period (from - to)"""
        left, right = view.enter_period(input, input)
        if mdl.check_validity_of_date(left) and mdl.check_validity_of_date(right):
            left = dt.datetime.strptime(left, "%d-%m-%Y").strftime('%Y-%m-%d %H:%M:%S')
            right = dt.datetime.strptime(right, "%d-%m-%Y").strftime('%Y-%m-%d %H:%M:%S')

            self.model.cursor.execute("SELECT SUM(length) FROM {db_name} WHERE date >= ? AND date <= ?".format(db_name=self.model.db_name), (left, right))
            sum_length = self.model.cursor.fetchone()[0]
            # print(self.model.cursor.fetchone())
            self.model.cursor.execute(
                "SELECT SUM(coef) FROM {db_name} WHERE date >= ? AND date <= ?".format(db_name=self.model.db_name), (left, right))
            sum_coef = self.model.cursor.fetchone()[0]
            cons = int(sum_length or 0) * int(sum_coef or 0) / 100
            print("\nTotal length: " + str(sum_length) +
                  "\nTotal consumption: " + str(sum_coef) +
                  "\nTotal fuel used: " + str(cons))
        else:
            view.invalid_value()

    def show_by_date(self, input_func=input):
        """show length ridden and fuel used by certain date"""
        date = view.enter_date(input_func)

        if mdl.check_validity_of_date(date):
            date = dt.datetime.strptime(date, "%d-%m-%Y").strftime('%Y-%m-%d')
            print(date)
            self.model.cursor.execute(
                "SELECT * FROM {db_name} WHERE date = ?".format(db_name=self.model.db_name), (date, ))
            records_daily = self.model.cursor.fetchall()
            view.record_names()
            if len(records_daily) > 0:
                for t in records_daily:
                    print(str(t[1]) + "\t\t" + str(t[2]) + "\t\t" + str(t[3]) + "\t\t\t\t" +
                          str(t[2] * t[3] / 100))
        else:
            view.invalid_value()

    def show_by_period(self):
        """show length ridden and fuel used by certain period (from - to)"""
        left, right = view.enter_period(input, input)
        if mdl.check_validity_of_date(left) and mdl.check_validity_of_date(right):
            left = dt.datetime.strptime(left, "%d-%m-%Y").strftime('%Y-%m-%d %H:%M:%S')
            right = dt.datetime.strptime(right, "%d-%m-%Y").strftime('%Y-%m-%d %H:%M:%S')

            self.model.cursor.execute(
                "SELECT SUM(length) FROM {db_name} WHERE date >= ? AND date <= ?".format(db_name=self.model.db_name),
                (left, right))
            table = self.model.cursor.fetchall()
            view.record_names()
            if len(table) > 0:
                for t in table:
                    print(str(t[1]) + "\t\t" + str(t[2]) + "\t\t" + str(t[3]) + "\t\t\t\t" +
                          str(t[2] * t[3] / 100))

        else:
            view.invalid_value()

    def add_record(self):
        """add new record to the database"""
        item_list = view.enter_trip_details(input, input, input)
        if mdl.check_validity(item_list):
            self.model.cursor.execute('INSERT INTO {} (date, length, coef) VALUES (?, ?, ?)'.format(self.model.db_name), item_list)
            self.model.conn.commit()
        else:
            view.invalid_value()