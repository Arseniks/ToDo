"""Обрабока результатов взаимодействия пользователя с интерфейсом."""
from uuid import uuid1

import dash
import requests
import uvicorn
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from todo.backend.schema import ToDo
from todo.backend.schema import Uuid
from todo.frontend import view

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
app.layout = view.TaskManager()

BASE_URL = "http://localhost:5001/"


def make_url(endpoint: str) -> str:
    """Формирует полный url запроса к endpoint."""
    return f"{BASE_URL}{endpoint}"


def data_and_selected(endpoint):
    """Получает данные из endpoint и формирует данные для таблички и перечень выбранных рядов."""
    data = requests.get(make_url(f"{endpoint}/")).json()
    selected_rows = []
    for num, todo in enumerate(data):
        uuid = todo.pop("uuid")
        todo["id"] = uuid
        if todo["done"]:
            selected_rows.append(num)
    return data, selected_rows


@app.callback(
    Output(component_id="Data", component_property="children"),
    [
        Input(component_id="Tabs", component_property="value"),
        Input(component_id="Button", component_property="children"),
    ],
)
def show_data(tab_name, _):
    """Загружает и отображает данные.

    При наличии сосздается таблица ToDo, а при отсутсвии сообщение об отсутсвии.
    """
    data, selected = data_and_selected(tab_name.lower())
    if data:
        table = view.TableToDo(data, selected)
    else:
        table = view.NoToDo()
    return table


@app.callback(
    Output(component_id="Tabs", component_property="value"),
    [Input(component_id="Table", component_property="selected_row_ids")],
    [
        State(component_id="Table", component_property="data"),
        State(component_id="Tabs", component_property="value"),
    ],
)
def toggle_todo(row_ids, data, tab_name):
    """Сохраняет на сервер изменение флага завершенности дела и обнавляет отбражение данных."""
    if row_ids is not None:
        row_ids = set(row_ids)
        for todo in data:
            if todo["id"] in row_ids and todo["done"] is False:
                requests.patch(make_url(f"toggle/"), Uuid(uuid=todo["id"]).json())
                return tab_name
            if todo["id"] not in row_ids and todo["done"] is True:
                requests.patch(make_url(f"toggle/"), Uuid(uuid=todo["id"]).json())
                return tab_name
    return tab_name


@app.callback(
    [
        Output(component_id="Name", component_property="value"),
        Output(component_id="Date", component_property="date"),
        Output(component_id="Description", component_property="value"),
        Output(component_id="Button", component_property="children"),
    ],
    [Input(component_id="Button", component_property="n_clicks")],
    [
        State(component_id="Name", component_property="value"),
        State(component_id="Date", component_property="date"),
        State(component_id="Description", component_property="value"),
    ],
)
def add_todo(_, name, date, description):
    """Добавляет ToDo в базу.

    Стирает информацию в диалоге и обнавляет отбражение данных.
    """
    if name is not None:
        requests.post(
            make_url(f"add/"),
            ToDo(uuid=uuid1(), name=name, date=date, done=False, description=description).json(),
        )
    return "", date, "", "ADD"


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app.server", interface="wsgi", host="0.0.0.0")
