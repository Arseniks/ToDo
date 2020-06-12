"""Обрабока результатов взаимодействия пользователя с интерфейсом."""
import dash
import requests
import uvicorn
from dash.dependencies import Input
from dash.dependencies import Output

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
    [
        Output(component_id="T_all", component_property="data"),
        Output(component_id="T_all", component_property="selected_rows"),
    ],
    [Input(component_id="T_all", component_property="data_timestamp")],
)
def get_all(timestamp):
    """Загрузка данных для вкладки All."""
    if timestamp is None:
        return data_and_selected("all")


@app.callback(
    Output(component_id="T_all", component_property="editable"),
    [Input(component_id="T_all", component_property="selected_row_ids")],
)
def get_all(selected_row_ids):
    """Загрузка данных для вкладки All."""
    print(selected_row_ids)
    return False


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app.server", interface="wsgi", host="0.0.0.0")

    # Постановка галочки (4 варианта) selected_rows
    # Переключение вкладок value
