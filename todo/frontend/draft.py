"""Интерфейс приложения приложения."""
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import uvicorn
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

task0 = [False, "a", "Собраться в школу", "2020-06-08", "Собрать еду и рюкзак"]
task1 = [True, "b", "Сходить в магазин", "2020-06-08", "Купить воду и сок"]
task2 = [True, "c", "Собраться в школу", "2020-06-07", "Собрать еду и рюкзак"]
task3 = [False, "d", "Сходить в магазин", "2020-06-07", "Купить тортик"]
task4 = [True, "e", "Сделать дз", "2020-06-09", "Математика и английский"]
task5 = [False, "f", "Сходить в аптеку", "2020-06-09", "Капли дляя носа"]

COLUMNS = ["Name", "Date", "Description"]
TYPE = ["text", "datetime", "text"]
OVERDUE = [task1]
TODAY = [task2]
PENDING = [task4]
ALL = [task0, task1, task2, task3, task4, task5]
DATA_ALL = [{name: value for name, value in zip(["id"] + COLUMNS, i[1:])} for i in ALL]

app = dash.Dash(__name__)


def main_html():
    app.layout = html.Div([html.H1("Tasks manager"), dcc.Tabs(id="tabs", value="All", vertical=True, children=get_tabs()), ])


def get_tabs():
    return [
        get_all_tab(),
        dcc.Tab(id="Overdue", label="Overdue", value="Overdue", ),
    ]


def get_all_tab():
    return dcc.Tab(label="All", value="All", children=[get_table(), *get_add_dialog()], )


def get_table():
    return dt.DataTable(
        id="T_all",
        columns=[{"name": col, "id": col, "type": types} for n, (col, types) in enumerate(zip(COLUMNS, TYPE))],
        data=DATA_ALL,
        editable=True,
        sort_action="native",
        row_selectable="multi",
        selected_rows=[n for n, i in enumerate(ALL) if i[0]],
        style_cell={"textAlign": "left", "whiteSpace": "normal", "maxWidth": 400},
        style_table={"overflowY": "auto"},
    )


def get_add_dialog():
    return [
        dcc.Input(placeholder="Name"),
        dcc.Textarea(placeholder="Description", style={"height": 100}),
        dcc.DatePickerSingle(display_format="YYYY-MM-DD", style={"borderRadius": "4px"}),
        html.Button("ADD", id="textarea-state-example-button"),
    ]


@app.callback(
    Output(component_id="Overdue", component_property="children"),
    [Input(component_id="T_all", component_property="data_timestamp")],
    [State(component_id="T_all", component_property="active_cell"), State(component_id="T_all", component_property="data"), ],
)
def controller(t, c, v):
    return print(t, c, v)


if __name__ == "__main__":
    main_html()
    uvicorn.run(f"{__name__}:app.server", interface="wsgi", host="0.0.0.0")
