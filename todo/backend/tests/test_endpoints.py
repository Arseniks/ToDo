from datetime import date
from datetime import timedelta
from uuid import uuid1

import pytest
from fastapi.testclient import TestClient

from todo.backend import schema
from todo.backend.endpoints import router
from todo.backend.schema import ToDo
from todo.backend.schema import Uuid


@pytest.fixture(scope="module", name="client")
def make_client():
    return TestClient(router)


def test_all_(tasks, client):
    response = client.get("/all/")
    assert response.status_code == 200
    assert list(map(lambda x: schema.ToDo(**x), response.json())) == tasks


def test_overdue(tasks, client):
    response = client.get("/overdue/")
    assert response.status_code == 200
    assert list(map(lambda x: schema.ToDo(**x), response.json())) == tasks[3:4]


def test_today(tasks, client):
    response = client.get("/today/")
    assert response.status_code == 200
    assert list(map(lambda x: schema.ToDo(**x), response.json())) == tasks[0:1]


def test_pending(tasks, client):
    response = client.get("/pending/")
    assert response.status_code == 200
    assert list(map(lambda x: schema.ToDo(**x), response.json())) == tasks[5:6]


def test_toggle_task(tasks, client):
    res = client.patch("/toggle/", data=Uuid(uuid=tasks[0].uuid).json())
    assert res.status_code == 200

    response = client.get("/today/")
    assert response.status_code == 200
    assert list(map(lambda x: schema.ToDo(**x), response.json())) == []


def test_add_task(tasks, client):
    new = ToDo.from_list(uuid1(), "Fix test", date.today() + timedelta(days=1), False)
    res = client.post("/add/", data=new.json())
    assert res.status_code == 200

    response = client.get("/pending/")
    assert response.status_code == 200
    assert list(map(lambda x: schema.ToDo(**x), response.json())) == tasks[5:6] + [new]
