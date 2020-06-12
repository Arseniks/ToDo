"""Обрабока результатов взаимодействия пользователя с интерфейсом."""
import dash
import uvicorn
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from todo.frontend import view

app = dash.Dash(__name__)


@app.callback(
    Output(component_id="T_overdue", component_property="children"),
    [Input(component_id="T_all", component_property="data_timestamp")],
    [
        State(component_id="T_all", component_property="active_cell"),
        State(component_id="T_all", component_property="data"),
    ],
)
def controller(t, c, v):
    return print(t, c, v)


if __name__ == "__main__":
    app.layout = view.TaskManager()

    uvicorn.run(f"{__name__}:app.server", interface="wsgi", host="0.0.0.0")

    # Постановка галочки (4 варианта) selected_rows
    # Изменение существующего задания (4 варианта) data_timestamp
    # Добавление таска n_clicks
    # Переключение вкладок value
