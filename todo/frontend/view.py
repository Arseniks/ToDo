from datetime import date

import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt


class TaskManager(html.Div):
    """HTML представление приложения по управлению ToDO."""

    def __init__(self):
        tabs = [
            Tab("Today"),
            Tab("Overdue"),
            Tab("Pending"),
            Tab("All"),
        ]

        super().__init__(
            [
                html.H1("Tasks manager"),
                dcc.Tabs(id="Tabs", vertical=True, children=tabs, value=None),
                Dialog(),
            ]
        )


class Tab(dcc.Tab):
    """Вкладка с таблицей с существующими ToDo."""

    def __init__(self, name):
        super().__init__(id=name, label=name, value=name)


class Table(dt.DataTable):
    """Таблица с существующими ToDo."""

    def __init__(self, name, data, selected_rows):
        super().__init__(
            id=f"T_{name}",
            columns=[
                {"name": "Name", "id": "name", "type": "text"},
                {"name": "Date", "id": "date", "type": "datetime"},
                {"name": "Description", "id": "description", "Description": "text"},
            ],
            data=data,
            selected_rows=selected_rows,
            editable=False,
            sort_action="native",
            row_selectable="multi",
            style_cell={"textAlign": "left", "whiteSpace": "normal"},
            style_table={"overflowY": "auto", "marginLeft": 6},
            style_as_list_view=True,
        )


class Dialog(html.Div):
    """Диалог для ввода нового ToDO."""

    def __init__(self):
        super().__init__(
            children=[
                html.H2("Add task"),
                dcc.Input(id="input", style={"marginTop": 0}, placeholder="Name"),
                dcc.DatePickerSingle(id="date", date=date.today(), display_format="YYYY-MM-DD"),
                dcc.Textarea(id="text", placeholder="Description", style={"height": 100}),
                html.Button(children="ADD", id="button"),
            ],
            style={"display": "flex", "flexFlow": "column wrap", "maxWidth": 480},
        )
