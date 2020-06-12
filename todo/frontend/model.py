"""Взаимодействие с REST сервером - сохранение и предоставление необходимых данных."""

"""Обрабока результатов взаимодействия пользователя с интерфейсом."""
import dash
import uvicorn
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from todo.frontend import view

app = dash.Dash(__name__)
app.layout = view.TaskManager()


@app.callback(
    Output(component_id="T_all", component_property="sort_action"),
    [Input(component_id="T_all", component_property="data_timestamp")],
    [
        State(component_id="T_all", component_property="active_cell"),
        State(component_id="T_all", component_property="data"),
    ],
)
def controller(t, c, v):
    return print(t, c, v)


@app.callback(
    Output(component_id="T_pending", component_property="sort_action"),
    [Input(component_id="T_pending", component_property="data_timestamp")],
    [
        State(component_id="T_pending", component_property="active_cell"),
        State(component_id="T_pending", component_property="data"),
    ],
)
def controller(t, c, v):
    return print(t, c, v)


@app.callback(
    Output(component_id="T_overdue", component_property="sort_action"),
    [Input(component_id="T_overdue", component_property="data_timestamp")],
    [
        State(component_id="T_overdue", component_property="active_cell"),
        State(component_id="T_overdue", component_property="data"),
    ],
)
def controller(t, c, v):
    return print(t, c, v)


@app.callback(
    Output(component_id="T_today", component_property="sort_action"),
    [Input(component_id="T_today", component_property="data_timestamp")],
    [
        State(component_id="T_today", component_property="active_cell"),
        State(component_id="T_today", component_property="data"),
    ],
)
def controller(t, c, v):
    return print(t, c, v)


@app.callback(
    [
        Output(component_id="input", component_property="value"),
        Output(component_id="date", component_property="date"),
        Output(component_id="text", component_property="value"),
    ],
    [Input(component_id="button", component_property="n_clicks")],
    [
        State(component_id="input", component_property="value"),
        State(component_id="date", component_property="date"),
        State(component_id="text", component_property="value"),
    ],
)
def controller(t, c, v, g):
    return print(t, c, v, g)


@app.callback(
    Output(component_id="T_all", component_property="style_as_list_view"),
    [Input(component_id="T_all", component_property="selected_rows")],
    [
        State(component_id="T_all", component_property="selected_rows"),
    ],
)
def controller(t, c, v):
    return print(t, c, v)


@app.callback(
    Output(component_id="T_pending", component_property="style_as_list_view"),
    [Input(component_id="T_pending", component_property="selected_rows")],
    [
        State(component_id="T_pending", component_property="selected_rows"),
    ],
)
def controller(t, c, v):
    return print(t, c, v)


@app.callback(
    Output(component_id="T_overdue", component_property="style_as_list_view"),
    [Input(component_id="T_overdue", component_property="selected_rows")],
    [
        State(component_id="T_overdue", component_property="selected_rows"),
    ],
)
def controller(t, c, v):
    return print(t, c, v)


@app.callback(
    Output(component_id="T_today", component_property="style_as_list_view"),
    [Input(component_id="T_today", component_property="selected_rows")],
    [
        State(component_id="T_today", component_property="selected_rows"),
    ],
)
def controller(t, c, v):
    return print(t, c, v)


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app.server", interface="wsgi", host="0.0.0.0")

    # Постановка галочки (4 варианта) selected_rows
    # Переключение вкладок value
