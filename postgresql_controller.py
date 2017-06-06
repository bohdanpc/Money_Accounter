import view
import postgresql.driver as pg_driver
import model as mdl
import _datetime as dt


class PostgreSQLController:

    def __init__(self):
        table_exist = False
        try:
            self.db = pg_driver.connect(user='postgres',
                                        password='root',
                                        host='localhost',
                                        port=5432)

            for table_name, in self.db.prepare("SELECT table_name FROM information_schema.tables"):
                print(table_name)
                if table_name == "fuel_consumption":
                    table_exist = True
                    break

            if not table_exist:
                self.db.execute("CREATE TABLE FUEL_CONSUMPTION (id SERIAL PRIMARY KEY, date DATE, length FLOAT, coef FLOAT)")
                print("TABLE CREATED")

            self.insert = self.db.prepare("INSERT INTO FUEL_CONSUMPTION (date, length, coef) VALUES ($1, $2, $3)")
            self.select_all = self.db.prepare("SELECT * FROM FUEL_CONSUMPTION")
            self.sum_length = self.db.prepare("SELECT SUM(length) FROM FUEL_CONSUMPTION")
            self.sum_coef = self.db.prepare("SELECT SUM(coef) FROM FUEL_CONSUMPTION")
            self.period = self.db.prepare("SELECT *  FROM FUEL_CONSUMPTION WHERE date > $1 AND date < $2")
            self.sum_period_length = self.db.prepare("SELECT SUM(length)  FROM FUEL_CONSUMPTION WHERE date > $1 AND date < $2")
            self.sum_period_coef = self.db.prepare("SELECT SUM(coef)  FROM FUEL_CONSUMPTION WHERE date > $1 AND date < $2")
            self.date = self.db.prepare("SELECT *  FROM FUEL_CONSUMPTION WHERE date = $1")
        except:
            print("no db connection")
            exit()

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

    def add_record(self):
        """add new record to the database"""
        item_list = view.enter_trip_details(input, input, input)
        if mdl.check_validity(item_list):
            self.insert(dt.datetime.strptime(item_list[0], "%d-%m-%Y"),
                        item_list[1],
                        item_list[2])
        else:
            view.invalid_value()

    def show_all(self):
        """show all present records in database"""
        table = self.select_all
        view.record_names()
        for t in table:
            print("\t\t" + str(t[1]) + "\t\t" + str(t[2]) + "\t\t" + str(t[3]) + "\t\t" +
                  str(t[2] * t[3] / 100))

    def show_summary(self):
        """show the sum of km's ridden and fuel used"""
        length = self.sum_length.first()
        coef = self.sum_coef.first()
        cons = length*coef/100
        print("Total length: " + str(length) +
              "\nTotal consumption: " + str(coef) +
              "\nTotal fuel used: " + str(cons))

    def show_by_period(self):
        """show length ridden and fuel used by certain period (from - to)"""
        left, right = view.enter_period(input, input)

        if mdl.check_validity_of_date(left) and mdl.check_validity_of_date(right):
            table = self.period(dt.datetime.strptime(left, "%d-%m-%Y"),
                                dt.datetime.strptime(right, "%d-%m-%Y"))

            view.record_names()
            for t in table:
                print("\t\t" + str(t[1]) + "\t\t" + str(t[2]) + "\t\t" + str(t[3]) + "\t\t" +
                      str(t[2]*t[3]/100))
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

if __name__ == "__main__":
    p = PostgreSQLController()
    p.run()
