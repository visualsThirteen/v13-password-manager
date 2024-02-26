import sqlite3
import json
import os


class DataProcessor:
    """
    Encapsulates functions for manipulations with database and json files.
    """
    DB_PATH = "pwm_data/password_manager.db"

    @staticmethod
    def create_database():
        """
        Creates database and password_manager table if not exists.
        """
        with sqlite3.connect(DataProcessor.DB_PATH) as con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS password_manager (app text, username text, password text)")
            con.commit()

    @staticmethod
    def insert_record(app: str, username: str, password: str):
        """
        Takes app name, username, password and adds to database.
        :param str app: Name of app or web page.
        :param str username: Username for app or web page.
        :param str password: Password for app or web page.
        """
        with sqlite3.connect(DataProcessor.DB_PATH) as con:
            cur = con.cursor()
            cur.execute(f"INSERT INTO password_manager VALUES (?,?,?)", (app, username, password))
            con.commit()

    @staticmethod
    def search_record(app: str) -> tuple or None:
        """
        Takes app name and searches for credentials in database. Returns credentials for specified app.
        :param str app: Name of app or web page.
        :return tuple or None: Tuple with first value as username and second value as password.
        If nothing was found, returns None.
        """
        with sqlite3.connect(DataProcessor.DB_PATH) as con:
            cur = con.cursor()
            cur.execute("SELECT username, password FROM password_manager WHERE app=?", (app,))
            values: tuple or None = cur.fetchone()
            return values

    @staticmethod
    def update_record(app: str, username: str, password: str):
        """
        Takes app name, username, password, updates username and password for specified app.
        :param str app: Name of app or web page.
        :param str username: Username for app or web page.
        :param str password: Password for app or web page.
        """
        with sqlite3.connect(DataProcessor.DB_PATH) as con:
            cur = con.cursor()
            cur.execute("""
            UPDATE password_manager 
            SET username=?, 
            password=? 
            WHERE app=?""",
                        (username, password, app)
                        )
            con.commit()

    @staticmethod
    def delete_table():
        """
        Deletes password_manager table.
        """
        with sqlite3.connect(DataProcessor.DB_PATH) as con:
            cur = con.cursor()
            cur.execute("DROP TABLE IF EXISTS password_manager")
            con.commit()

    @staticmethod
    def save_preferences(data: dict):
        """
        Takes data as dictionary and saves to data.json file. If file not exists, creates one.
        :param data: Dictionary containing user preferences.
        """
        content: dict = {}
        try:
            with open("pwm_data/data.json") as data_file:
                content = json.load(data_file)
            content.update(data)
        except (FileNotFoundError, ValueError):
            content = data
        finally:
            with open("pwm_data/data.json", "w") as data_file:
                json.dump(content, data_file, indent=4)

    @staticmethod
    def load_preferences() -> dict or None:
        """
        Loads and returns user preferences from data.json file as dictionary, if nothing found,
        returns None.
        :return dict or None: Dictionary or None.
        """
        try:
            with open("pwm_data/data.json") as data_file:
                data = json.load(data_file)
                return data
        except (FileNotFoundError, ValueError):
            return None

    @staticmethod
    def delete_preferences():
        """
        Deletes data.json file if exists.
        """
        if os.path.exists("pwm_data/data.json"):
            os.remove("pwm_data/data.json")

    @staticmethod
    def get_all_apps() -> list:
        """
        Returns list of all apps in database.
        :return list: All apps in database.
        """
        with sqlite3.connect(DataProcessor.DB_PATH) as con:
            cur = con.cursor()
            cur.execute("SELECT app FROM password_manager")
            values = cur.fetchall()
            return values
