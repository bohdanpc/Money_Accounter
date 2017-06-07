from model import Model
from controller import Controler
from configparser import ConfigParser
from postgresql_controller import PostgreSQLController
from sqlite_controller import SQLiteController
from mysql_controller import MysqlController

if __name__ == "__main__":
    config = ConfigParser()
    config.read("ini")
    db_type = config["db-selection"]["db"]
    file_name = "FUEL_CONSUMPTION"

    if db_type == "pickle":
        controller = Controler(Model())
    elif db_type == "sqlite":
        controller = SQLiteController(Model())
    elif db_type == "postgres":
        controller = PostgreSQLController()
    elif db_type == "mysql":
        controller = MysqlController()

    controller.run()
