from model import Model
from controller import Controler
from configparser import ConfigParser
from postgresql_controller import PostgreSQLController

if __name__ == "__main__":
    config = ConfigParser()
    config.read("ini")
    db_type = config["db-selection"]["db"]
    file_name = "fuel_consumption"

    if db_type == "pickle":
        controller = Controler(Model)
    elif db_type == "postgres":
        controller = PostgreSQLController()

    controller.run()
