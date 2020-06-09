from datetime import date
from datetime import timedelta
from uuid import uuid1

import pytest

from todo.backend import config
from todo.backend import database
from todo.backend.schema import ToDo


def get_today_date():
    today = date.today()
    return today


def get_tomorrow_date():
    tomorrow = get_today_date() + timedelta(days=1)
    return tomorrow


def get_yesterday_date():
    yesterday = get_today_date() - timedelta(days=1)
    return yesterday


@pytest.fixture(name="tasks")
def make_db(monkeypatch, tmp_path):
    monkeypatch.setattr(database.get_conn, "_conn", None)
    monkeypatch.setattr(config, "DB_PATH", tmp_path / "ToDo.db")

    task0 = ToDo.from_list(uuid1(), "Собраться в школу", get_today_date(), False, "Собрать еду и рюкзак")
    task1 = ToDo.from_list(uuid1(), "Сходить в магазин", get_today_date(), True, "Купить воду и сок")
    task2 = ToDo.from_list(uuid1(), "Собраться в школу", get_yesterday_date(), True, "Собрать еду и рюкзак")
    task3 = ToDo.from_list(uuid1(), "Сходить в магазин", get_yesterday_date(), False, "Купить тортик")
    task4 = ToDo.from_list(uuid1(), "Сделать дз", get_tomorrow_date(), True, "Математика и английский")
    task5 = ToDo.from_list(uuid1(), "Сходить в аптеку", get_tomorrow_date(), False, "Капли дляя носа")

    database.add_task(task0)
    database.add_task(task1)
    database.add_task(task2)
    database.add_task(task3)
    database.add_task(task4)
    database.add_task(task5)

    yield [task0, task1, task2, task3, task4, task5]
