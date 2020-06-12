"""Обрабока результатов взаимодействия пользователя с интерфейсом."""
import dash
import dash_html_components as html
import requests
import uvicorn
from dash.dependencies import Input
from dash.dependencies import Output
from dash.exceptions import PreventUpdate

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
        Output(component_id="Today", component_property="children"),
        Output(component_id="Overdue", component_property="children"),
        Output(component_id="Pending", component_property="children"),
        Output(component_id="All", component_property="children"),
    ],
    [Input(component_id="Tabs", component_property="value")],
)
def load_data(value):
    """Загрузка данных для вкладки All."""
    if value is None:
        tables = []
        for name in ["Today", "Overdue", "Pending", "All"]:
            data, selected = data_and_selected(name.lower())
            if data:
                table = view.Table(name, data, selected)
            else:
                table = html.H2(f"No todo", style={"marginLeft": 6}, )
            tables.append(table)
        return tables
    raise PreventUpdate


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app.server", interface="wsgi", host="0.0.0.0")

    # Постановка галочки (4 варианта) selected_rows
    # Переключение вкладок value
