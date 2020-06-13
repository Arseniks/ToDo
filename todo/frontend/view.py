from datetime import date

import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt


class TaskManager(html.Div):
    """HTML представление приложения по управлению ToDO."""

    def __init__(self):
        super().__init__([html.H1("Tasks manager"), Tabs(), html.Div(id="Data"), Dialog()])


class Tabs(dcc.Tabs):
    """Набор вкладок с разными представленими дел."""

    def __init__(self):
        tabs = [
            Tab("Today"),
            Tab("Overdue"),
            Tab("Pending"),
            Tab("All"),
        ]
        super().__init__(id="Tabs", vertical=False, children=tabs, value="Today")


class Tab(dcc.Tab):
    """Вкладка с таблицей с существующими ToDo."""

    def __init__(self, name):
        super().__init__(label=name, value=name)


class NoToDo(html.H2):
    """Сообщение об остсутсвии ToDo в данном представлении.."""

    def __init__(self):
        super().__init__("No todo", style={"marginLeft": 6})


class TableToDo(dt.DataTable):
    """Таблица с существующими ToDo."""

    def __init__(self, data, selected_rows):
        super().__init__(
            id=f"Table",
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
            style_table={"overflowY": "auto", "marginLeft": 6, "marginTop": 18},
            style_as_list_view=True,
        )


class Dialog(html.Div):
    """Диалог для ввода нового ToDo."""

    def __init__(self):
        super().__init__(
            children=[
                html.H2("Add task"),
                dcc.Input(id="Name", style={"marginTop": 0}, placeholder="Name"),
                dcc.DatePickerSingle(id="Date", date=date.today(), display_format="YYYY-MM-DD"),
                dcc.Textarea(id="Description", placeholder="Description", style={"height": 100}),
                html.Button(id="Button", children="ADD", ),
            ],
            style={"display": "flex", "flexFlow": "column wrap", "maxWidth": 480},
        )
