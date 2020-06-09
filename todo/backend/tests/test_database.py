from datetime import date
from datetime import timedelta
from uuid import uuid1

import pytest

from backend import database
from backend import schema


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
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "ToDo.db")

    task0 = schema.ToDo.from_list(uuid1(), "Собраться в школу", get_today_date(), False, "Собрать еду и рюкзак")
    task1 = schema.ToDo.from_list(uuid1(), "Сходить в магазин", get_today_date(), True, "Купить воду и сок")
    task2 = schema.ToDo.from_list(uuid1(), "Собраться в школу", get_yesterday_date(), True, "Собрать еду и рюкзак")
    task3 = schema.ToDo.from_list(uuid1(), "Сходить в магазин", get_yesterday_date(), False, "Купить тортик")
    task4 = schema.ToDo.from_list(uuid1(), "Сделать дз", get_tomorrow_date(), True, "Математика и английский")
    task5 = schema.ToDo.from_list(uuid1(), "Сходить в аптеку", get_tomorrow_date(), False, "Капли дляя носа")

    database.add_task(task0)
    database.add_task(task1)
    database.add_task(task2)
    database.add_task(task3)
    database.add_task(task4)
    database.add_task(task5)

    yield [task0, task1, task2, task3, task4, task5]


def test_get_all(tasks):
    assert tasks == database.get_all()


def test_get_overdue_tasks(tasks):
    assert tasks[3:4] == database.get_overdue_tasks()


def test_get_today_tasks(tasks):
    assert tasks[0:1] == database.get_today_tasks()


def test_get_pending_tasks(tasks):
    assert tasks[5:6] == database.get_pending_tasks()


def test_toggle_task(tasks):
    assert tasks[5:6] == database.get_pending_tasks()
    database.toggle_task(tasks[5].uuid)
    assert [] == database.get_pending_tasks()
    database.toggle_task(tasks[5].uuid)
    assert tasks[5:6] == database.get_pending_tasks()


def test_reopen_db(tasks, monkeypatch):
    assert tasks == database.get_all()
    monkeypatch.setattr(database.get_conn, "_conn", None)
    print(database.get_all()[0].to_list())
    assert tasks == database.get_all()
