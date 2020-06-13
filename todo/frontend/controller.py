"""Обрабока результатов взаимодействия пользователя с интерфейсом."""
from typing import Callable
from typing import List
from typing import NoReturn
from typing import Optional
from typing import Union
from uuid import uuid1

import requests
from dash import Dash
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from pydantic import BaseModel

from todo import config
from todo.backend.schema import ToDo
from todo.backend.schema import Uuid
from todo.frontend import view

CONTROLLERS = []
BASE_URL = f"{config.BACKEND_URL}:{config.BACKEND_PORT}/"


def make_url(endpoint: str) -> str:
    """Формирует полный url запроса к endpoint."""
    return f"{BASE_URL}{endpoint}"


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


def save_toggle_task(uuid: str):
    """Сохраняет на сервер изменение флага завершенности дела."""
    requests.patch(make_url(f"toggle/"), Uuid(uuid=uuid).json())


def save_task(name: str, date: str, description: str):
    """Сохраняет новое ToDo на сервер."""
    todo = ToDo(uuid=uuid1(), name=name, date=date, done=False, description=description)
    requests.post(make_url(f"add/"), todo.json())


class Controller(BaseModel):
    """Описание контроллера для Dash."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        CONTROLLERS.append(self)

    output: Union[Output, List[Output]]
    inputs: List[Input]
    state: Optional[List[State]] = []
    func: Callable

    class Config:
        arbitrary_types_allowed = True


def show_data(tab_name, _):
    """Загружает и отображает данные.

    При наличии сосздается таблица ToDo, а при отсутсвии сообщение об отсутсвии.
    """
    data, selected = load_data_and_selected(tab_name.lower())
    if data:
        table = view.TableToDo(data, selected)
    else:
        table = view.NoToDo()
    return table


Controller(
    output=Output(component_id="Data", component_property="children"),
    inputs=[
        Input(component_id="Tabs", component_property="value"),
        Input(component_id="Button", component_property="children"),
    ],
    func=show_data,
)


def toggle_todo(row_ids, data, tab_name):
    """Обрабатывает изменение флага завершенности дела и обнавляет отбражение данных."""
    if row_ids is not None:
        row_ids = set(row_ids)
        for todo in data:
            uuid = todo["id"]
            done = todo["done"]
            if (uuid in row_ids and done is False) or (uuid not in row_ids and done is True):
                save_toggle_task(uuid)
                break
    return tab_name


Controller(
    output=Output(component_id="Tabs", component_property="value"),
    inputs=[Input(component_id="Table", component_property="selected_row_ids")],
    state=[
        State(component_id="Table", component_property="data"),
        State(component_id="Tabs", component_property="value"),
    ],
    func=toggle_todo,
)


def add_todo(_, name, date, description):
    """Обрабатывает добавление ToDo.

    Стирает информацию в диалоге и обнавляет отбражение данных.
    """
    if name is not None:
        save_task(name, date, description)
    return "", date, "", "ADD"


Controller(
    output=[
        Output(component_id="Name", component_property="value"),
        Output(component_id="Date", component_property="date"),
        Output(component_id="Description", component_property="value"),
        Output(component_id="Button", component_property="children"),
    ],
    inputs=[Input(component_id="Button", component_property="n_clicks")],
    state=[
        State(component_id="Name", component_property="value"),
        State(component_id="Date", component_property="date"),
        State(component_id="Description", component_property="value"),
    ],
    func=add_todo,
)


def activate_all(dash: Dash) -> NoReturn:
    """Активирует все контролерры для указанного Dash-приложения."""
    for controller in CONTROLLERS:
        kwargs = controller.dict()
        func = kwargs.pop("func")
        dash.callback(**kwargs)(func)
