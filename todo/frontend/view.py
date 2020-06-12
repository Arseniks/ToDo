from datetime import date

import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt


class TaskManager(html.Div):
    """HTML представление приложения по управлению ToDO."""

    def __init__(self):
        tabs = [
            TableTab("Today"),
            TableTab("Overdue"),
            TableTab("Pending"),
            TableTab("All"),
        ]

        super().__init__(
            [
                html.H1("Tasks manager"),
                dcc.Tabs(id="tabs", value="Overdue", vertical=True, children=tabs),
                Dialog(),
            ]
        )


class TableTab(dcc.Tab):
    """Таблица с существующими ToDo."""

    def __init__(self, name):
        table = dt.DataTable(
            id=f"T_{name.lower()}",
            columns=[
                {"name": "Name", "id": "name", "type": "text"},
                {"name": "Date", "id": "date", "type": "datetime"},
                {"name": "Description", "id": "description", "Description": "text"},
            ],
            editable=False,
            sort_action="native",
            row_selectable="multi",
            style_cell={"textAlign": "left", "whiteSpace": "normal"},
            style_table={"overflowY": "auto", "marginLeft": 6},
            style_as_list_view=True,
        )
        super().__init__(
            id=f"Tab_{name.lower()}", label=name, value=name, children=table,
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
