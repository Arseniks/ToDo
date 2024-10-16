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
        super().__init__([
            html.H1("Менеджер задач"),
            Search(),
            html.Div(id="SearchData", style={"margin": 20}),
            Tabs(),
            html.Div(id="Data"),
            Dialog()
        ])


class Search(html.Div):
    """Входные данные для поиска по ToDo."""
    def __init__(self):
            super().__init__(
                children=[
                    dcc.Input(id="SearchName", placeholder="Название"),
                    dcc.DatePickerSingle(id="SearchDate", display_format="YYYY-MM-DD"),
                    dcc.Input(id="SearchDescription", placeholder="Описание"),
                    html.Button(id="SearchButton", children="Поиск"),
                ],
                style={"display": "flex", "flexFlow": "column wrap", "maxWidth": 480, "maxHeight": 80, "textAlign": "right", "margin": 20},
            )

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
            id="Table",
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
                dcc.Input(id="Name", style={"marginTop": 0}, placeholder="Название"),
                dcc.DatePickerSingle(id="Date", date=date.today(), display_format="YYYY-MM-DD"),
                dcc.Textarea(id="Description", placeholder="Описание", style={"height": 100}),
                html.Button(id="Button", children="ДОБАВИТЬ"),
            ],
            style={"display": "flex", "flexFlow": "column wrap", "maxWidth": 480},
        )
