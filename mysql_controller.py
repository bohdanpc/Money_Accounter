import view
import warnings
import MySQLdb
import model as mdl
import _datetime as dt

class MysqlController:
    dbname = "lab4zam"
    tablename = "fuel_consumption"
    def __init__(self):
        self.dbcon = MySQLdb.connect(host="localhost", user="root", passwd="mysqlsqlpass359359", charset='utf8')
        self.cursor = self.dbcon.cursor()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.cursor.execute("create database if not exists " + self.dbname)
            self.cursor.execute("use " + self.dbname)
            self.cursor.execute("create table if not exists " + self.tablename + "(id serial primary key, date date, length float, coef float, fuel_used float)")             

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
        self.cursor.close()
        self.dbcon.close()

    def add_record(self):
        """add new record to the database"""
        item_list = view.enter_trip_details(input, input, input)
        if mdl.check_validity(item_list):            
            self.cursor.execute("insert into " + self.tablename + " (date, length, coef, fuel_used) values (%s, %s, %s, %s)",
                                [dt.datetime.strptime(item_list[0], "%d-%m-%Y").strftime('%Y-%m-%d %H:%M:%S'),
                                 item_list[1],
                                 item_list[2],
                                 item_list[1] * item_list[2] / 100])
            self.dbcon.commit()
        else:
            view.invalid_value()


    def show_all(self):
        """show all present records in database"""
        self.cursor.execute("select * from " + self.tablename)
        table = self.cursor.fetchall()
        view.record_names()
        for row in table:
            print("%10s|%10s|%18s|%10s|"%(str(row[1]),  str(row[2]),  str(row[3]), str(row[4])))

    def show_summary(self):
        """show the sum of km's ridden and fuel used"""
        self.cursor.execute("select sum(length) from " + self.tablename)
        length = self.cursor.fetchall()[0][0]
        self.cursor.execute("select sum(fuel_used) from " + self.tablename)
        used = self.cursor.fetchall()[0][0]
        view.print_summary(length, used)

    def show_by_period(self):
        """show length ridden and fuel used by certain period (from - to)"""
        left, right = view.enter_period(input, input)

        if mdl.check_validity_of_date(left) and mdl.check_validity_of_date(right):
            left = dt.datetime.strptime(left, "%d-%m-%Y").strftime('%Y-%m-%d %H:%M:%S')
            right = dt.datetime.strptime(right, "%d-%m-%Y").strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute("select *  from " + self.tablename + " where date >= %s and date <= %s",
                                (left, right))
            table = self.cursor.fetchall()
            view.record_names()
            for row in table:
                print("%10s|%10s|%18s|%10s|"%(str(row[1]),  str(row[2]),  str(row[3]), str(row[4])))
        else:
            view.invalid_value()

    def show_summary_period(self):
        """show the sum of km's ridden and fuel used
                   in date period (from - to)"""
        left, right = view.enter_period(input, input)

        if mdl.check_validity_of_date(left) and mdl.check_validity_of_date(right):
            length = self.sum_period_length(dt.datetime.strptime(left, "%d-%m-%Y"),
                                            dt.datetime.strptime(right, "%d-%m-%Y"))[0][0]
            coef = self.sum_period_coef(dt.datetime.strptime(left, "%d-%m-%Y"),
                                        dt.datetime.strptime(right, "%d-%m-%Y"))[0][0]
            cons = int(length or 0) * int(coef or 0) / 100
            print("Total length: " + str(length) +
                  "\nTotal consumption: " + str(coef) +
                  "\nTotal fuel used: " + str(cons))
        else:
            view.invalid_value()

    def show_by_date(self):
        """show length ridden and fuel used by certain date"""
        date = view.enter_date(input)
        if mdl.check_validity_of_date(date):
            table = self.date(dt.datetime.strptime(date, "%d-%m-%Y"))
            view.record_names()
            for t in table:
                print("\t\t" + str(t[1]) + "\t\t" + str(t[2]) + "\t\t" + str(t[3]) + "\t\t" +
                      str(t[2] * t[3] / 100))
        else:
            view.invalid_value()
