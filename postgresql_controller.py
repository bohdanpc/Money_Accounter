import postgresql
import postgresql.driver as pg_driver
import _datetime as dt

class PostgreSQLController:

    def __init__(self):
        try:
            self.db = pg_driver.connect(user='postgres',
                                        password='root',
                                        host='localhost',
                                        port=5432)

            self.insert = self.db.prepare("INSERT INTO FUEL_CONSUMPTION (date, length, coef) VALUES ($1, $2, $3)")
            self.select_all = self.db.prepare("SELECT * FROM FUEL_CONSUMPTION")
            self.sum_length = self.db.prepare("SELECT SUM(length) FROM FUEL_CONSUMPTION")
            self.sum_coef = self.db.prepare("SELECT SUM(coef) FROM FUEL_CONSUMPTION")
        except:
            print("no db connection")
            return

        #self.db.execute("CREATE TABLE FUEL_CONSUMPTION (id SERIAL PRIMARY KEY, date DATE, length INT, coef INT)")

    def add_new(self, d, l, c):
        self.insert(d, l, c)

    def show_all(self):
        table = self.select_all
        for t in table:
            print(str(t[1])+"\t\t"+str(t[2])+"\t\t"+str(t[3])+"\t\t")

    def show_sumary(self):
        print(str(self.sum_length.first())+" "+str(self.sum_coef.first()))


if __name__ == "__main__":
    p = PostgreSQLController()
    #p.add_new(dt.datetime.now(), 2, 1)
    p.show_all()
    p.show_sumary()