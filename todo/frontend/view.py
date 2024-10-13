""""Элементы визуального представления Web приложения."""
from datetime import date

from dash import dcc
from dash import html
from dash import dash_table as dt


class TaskManager(html.Div):
    """HTML представление приложения по управлению ToDO.

    - заголовок
    - вкладки для переключения между разными представлениями ToDo
    - блок с данными о ToDo
    - диалог для добавления ToDo
    """

    def __init__(self):
        super().__init__([html.H1("Менеджер задач"), Tabs(), html.Div(id="Data"), Dialog()])


class Tabs(dcc.Tabs):
    """Набор вкладок для переключения между разными представлениями ToDo."""

    def __init__(self):
        tabs = [
            Tab("Сегодня", "Today"),
            Tab("Просроченные","Overdue"),
            Tab("Ожидающие", "Pending", ),
            Tab("Все", "All", ),
        ]
        super().__init__(id="Tabs", vertical=False, children=tabs, value="Today")


class Tab(dcc.Tab):
    """Вкладка для выбора представления ToDo."""

    def __init__(self, label, name):
        super().__init__(label=label, value=name)


class NoToDo(html.H2):
    """Сообщение об остсутсвии ToDo в данном представлении."""

    def __init__(self):
        super().__init__("No todo", style={"marginLeft": 6})


class TableToDo(dt.DataTable):
    """Таблица с существующими ToDo."""

    def __init__(self, data, selected_rows):
        super().__init__(
            id=f"Table",
            columns=[
                {"name": "Имя", "id": "name", "type": "text"},
                {"name": "Дата", "id": "date", "type": "datetime"},
                {"name": "Описание", "id": "description", "Description": "text"},
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
                dcc.Input(id="Name", style={"marginTop": 0}, placeholder="Названия"),
                dcc.DatePickerSingle(id="Date", date=date.today(), display_format="YYYY-MM-DD"),
                dcc.Textarea(id="Description", placeholder="Описание", style={"height": 100}),
                html.Button(id="Button", children="ДОБАВИТЬ"),
            ],
            style={"display": "flex", "flexFlow": "column wrap", "maxWidth": 480},
        )
