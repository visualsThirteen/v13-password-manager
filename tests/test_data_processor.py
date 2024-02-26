from v13pwm.data_processor import DataProcessor
import pytest
import sqlite3
import os

DEMO_RECORDS = {
    "app": "test_app",
    "app_2": "test_app_2",
    "app_3": "test_app_3",
    "username": "test_username",
    "password": "test_password",
    "upd_username": "up_test_username",
    "upd_password": "upd_test_password",
}


@pytest.fixture(scope="session")
def custom_database():
    custom_db_path = "test_pwm.db"
    DataProcessor.DB_PATH = custom_db_path
    yield
    if os.path.exists(custom_db_path):
        os.remove(custom_db_path)


def test_create_database(custom_database):
    DataProcessor.create_database()

    with sqlite3.connect(DataProcessor.DB_PATH) as con:
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='password_manager'")
        assert cur.fetchone() is not None


def test_insert_record(custom_database):
    DataProcessor.insert_record(
        app=DEMO_RECORDS["app"],
        username=DEMO_RECORDS["username"],
        password=DEMO_RECORDS["password"]
    )

    with sqlite3.connect(DataProcessor.DB_PATH) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM password_manager")
        assert cur.fetchall() is not None


def test_search_record(custom_database):
    values = DataProcessor.search_record(app=DEMO_RECORDS["app"])
    assert values[0] == DEMO_RECORDS["username"]
    assert values[1] == DEMO_RECORDS["password"]


def test_search_record_invalid(custom_database):
    values = DataProcessor.search_record("Non-existent")
    assert values is None


def test_update_record(custom_database):
    DataProcessor.update_record(
        app=DEMO_RECORDS["app"],
        username=DEMO_RECORDS["upd_username"],
        password=DEMO_RECORDS["upd_password"]
    )
    values = DataProcessor.search_record(DEMO_RECORDS["app"])
    assert values[0] == DEMO_RECORDS["upd_username"]
    assert values[1] == DEMO_RECORDS["upd_password"]


def test_get_all_apps(custom_database):
    DataProcessor.insert_record(
        app=DEMO_RECORDS["app_2"],
        username=DEMO_RECORDS["username"],
        password=DEMO_RECORDS["password"]
    )
    DataProcessor.insert_record(
        app=DEMO_RECORDS["app_3"],
        username=DEMO_RECORDS["username"],
        password=DEMO_RECORDS["password"]
    )
    values = DataProcessor.get_all_apps()
    assert len(values) == 3
    assert values[0][0] == DEMO_RECORDS["app"]
    assert values[1][0] == DEMO_RECORDS["app_2"]
    assert values[2][0] == DEMO_RECORDS["app_3"]


def test_delete_table(custom_database):
    DataProcessor.delete_table()
    with sqlite3.connect(DataProcessor.DB_PATH) as con:
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='password_manager'")
        assert cur.fetchone() is None
