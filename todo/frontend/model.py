"""Взаимодействие с REST сервером - сохранение и предоставление необходимых данных."""
from uuid import uuid1

import requests
from fastapi import Query

from todo import config
from todo.backend.schema import ToDo, SearchData
from todo.backend.schema import Uuid


def make_url(endpoint: str) -> str:
    """Формирует полный url запроса к endpoint."""
    return f"{config.BACKEND_URL_WITH_PORT}/{endpoint}"


def load_data_and_selected(endpoint: str):
    """Получает данные c сервера и формирует данные для таблички и перечень выбранных рядов."""
    data = requests.get(make_url(f"{endpoint}/")).json()
    selected_rows = []
    for num, todo in enumerate(data):
        uuid = todo.pop("uuid")
        todo["id"] = uuid
        if todo["done"]:
            selected_rows.append(num)
    return data, selected_rows

def search_task(name, date, description):
    """Получает данные c сервера по входным данным и формирует данные для таблички и перечень выбранных рядов."""
    todo = SearchData(name=name, date=date, description=description)
    data = requests.post(make_url("search/"), todo.json()).json()
    selected_rows = []
    for num, todo in enumerate(data):
        uuid = todo.pop("uuid")
        todo["id"] = uuid
        if todo["done"]:
            selected_rows.append(num)
    return data, selected_rows


def save_toggle_task(uuid: str):
    """Сохраняет на сервер изменение флага завершенности дела."""
    requests.patch(make_url("toggle/"), Uuid(uuid=uuid).json())


def save_task(name: str, date: str, description: str):
    """Сохраняет новое ToDo на сервер."""
    todo = ToDo(uuid=uuid1(), name=name, date=date, done=False, description=description)
    requests.post(make_url("add/"), todo.json())
