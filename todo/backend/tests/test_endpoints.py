from datetime import date
from datetime import timedelta
from uuid import uuid1

import pytest
from fastapi.testclient import TestClient

from todo.backend import database
from todo.backend import schema
from todo.backend.endpoints import router
from todo.backend.schema import Uuid

client = TestClient(router)


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

    task0 = {'uuid': str(uuid1()), 'name': 'Собраться в школу', 'date': get_today_date(), 'done': False,
             'description': 'Собрать еду и рюкзак'}
    task1 = {'uuid': str(uuid1()), 'name': 'Сходить в магазин', 'date': get_today_date(), 'done': True,
             'description': 'Купить воду и сок'}
    task2 = {'uuid': str(uuid1()), 'name': 'Собраться в школу', 'date': get_yesterday_date(), 'done': True,
             'description': 'Собрать еду и рюкзак'}
    task3 = {'uuid': str(uuid1()), 'name': 'Сходить в магазин', 'date': get_yesterday_date(), 'done': False,
             'description': 'Купить тортик'}
    task4 = {'uuid': str(uuid1()), 'name': 'Сделать дз', 'date': get_tomorrow_date(), 'done': True,
             'description': 'Математика и английский'}
    task5 = {'uuid': str(uuid1()), 'name': 'Сходить в аптеку', 'date': get_tomorrow_date(), 'done': False,
             'description': 'Капли для носа'}

    client.post('/add/', data=schema.ToDo(**task0).json())
    client.post('/add/', data=schema.ToDo(**task1).json())
    client.post('/add/', data=schema.ToDo(**task2).json())
    client.post('/add/', data=schema.ToDo(**task3).json())
    client.post('/add/', data=schema.ToDo(**task4).json())
    client.post('/add/', data=schema.ToDo(**task5).json())

    yield [task0, task1, task2, task3, task4, task5]


def test_all_(tasks):
    response = client.get("/all/")
    assert response.status_code == 200
    response = response.json()
    for i in response:
        date_ = date.fromisoformat(i['date'])
        i['date'] = date_
    assert response == tasks


def test_overdue(tasks):
    response = client.get("/overdue/")
    assert response.status_code == 200
    response = response.json()
    for i in response:
        date_ = date.fromisoformat(i['date'])
        i['date'] = date_
    assert response == tasks[3:4]


def test_today(tasks):
    response = client.get("/today/")
    assert response.status_code == 200
    response = response.json()
    for i in response:
        date_ = date.fromisoformat(i['date'])
        i['date'] = date_
    assert response == tasks[0:1]


def test_pending(tasks):
    response = client.get("/pending/")
    assert response.status_code == 200
    response = response.json()
    for i in response:
        date_ = date.fromisoformat(i['date'])
        i['date'] = date_
    assert response == tasks[5:6]


def test_toggle_task(tasks):
    res = client.patch("/toggle/", data=Uuid(uuid=tasks[0]['uuid']).json())
    assert res.status_code == 200
    response = client.get("/today/")
    assert response.status_code == 200
    response = response.json()
    for i in response:
        date_ = date.fromisoformat(i['date'])
        i['date'] = date_
    assert response != tasks[0:1]
