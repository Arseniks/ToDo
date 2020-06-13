"""Обрабока результатов взаимодействия пользователя с интерфейсом."""
import dash
import requests
import uvicorn
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from todo.frontend import view

app = dash.Dash(__name__)
app.layout = view.TaskManager()

BASE_URL = "http://0.0.0.0:5001/"


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
    [Input(component_id="Tabs", component_property="value")],
)
def show_data(tab_name):
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
    Output(component_id="Table", component_property="sort_action"),
    [Input(component_id="Table", component_property="selected_row_ids")],
    [State(component_id="Table", component_property="data")],
)
def toggle_todo(row_ids, data):
    """Сохраняет на сервер изменение флага завершенности дела."""
    print(row_ids, data)
    return "native"


@app.callback(
    [
        Output(component_id="Name", component_property="value"),
        Output(component_id="Date", component_property="date"),
        Output(component_id="Description", component_property="value"),
        Output(component_id="Tabs", component_property="value"),
    ],
    [Input(component_id="Button", component_property="n_clicks")],
    [
        State(component_id="Name", component_property="value"),
        State(component_id="Date", component_property="date"),
        State(component_id="Description", component_property="value"),
        State(component_id="Tabs", component_property="value"),
    ],
)
def add_todo(_, name, date, description, tab_name):
    """Добавляет ToDo в базу.

    Стирает информацию в диалоге и обнавляет отбражение данных.
    """
    print(_, name, date, description, tab_name)
    return "", date, "", tab_name


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app.server", interface="wsgi", host="0.0.0.0")

    # Редактирование???
