"""Обрабока результатов взаимодействия пользователя с интерфейсом."""
from typing import Callable
from typing import List
from typing import NoReturn
from typing import Optional
from typing import Union

from dash import Dash
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from pydantic import BaseModel

from todo.frontend import model
from todo.frontend import view

CONTROLLERS = []


class Controller(BaseModel):
    """Описание контроллера для Dash."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        CONTROLLERS.append(self)

    output: Union[Output, List[Output]]
    inputs: List[Input]
    state: Optional[List[State]] = []
    func: Callable

    class Config:
        arbitrary_types_allowed = True


def search_todo(_, name, date, description):
    """Ищет дела по входным данным.

    При наличии создается таблица ToDo, а при отсутсвии сообщение об отсутсвии.
    """
    table = view.NoToDo()
    if name is not None:
        data, selected = model.search_task(name, date, description)

        if data:
            table = view.TableToDo(data, selected)

    return "", date, "", "ПОИСК", table


Controller(
    output=[
        Output(component_id="SearchName", component_property="value"),
        Output(component_id="SearchDate", component_property="date"),
        Output(component_id="SearchDescription", component_property="value"),
        Output(component_id="SearchButton", component_property="children"),
        Output(component_id="SearchData", component_property="children"),
    ],
    inputs=[Input(component_id="SearchButton", component_property="n_clicks")],
    state=[
        State(component_id="SearchName", component_property="value"),
        State(component_id="SearchDate", component_property="date"),
        State(component_id="SearchDescription", component_property="value"),
    ],
    func=search_todo,
)


def show_data(tab_name, _):
    """Загружает и отображает данные.

    При наличии создается таблица ToDo, а при отсутсвии сообщение об отсутсвии.
    """
    data, selected = model.load_data_and_selected(tab_name.lower())
    if data:
        table = view.TableToDo(data, selected)
    else:
        table = view.NoToDo()
    return table


Controller(
    output=Output(component_id="Data", component_property="children"),
    inputs=[
        Input(component_id="Tabs", component_property="value"),
        Input(component_id="Button", component_property="children"),
    ],
    func=show_data,
)


def toggle_todo(row_ids, data, tab_name):
    """Обрабатывает изменение флага завершенности дела и обнавляет отбражение данных."""
    if row_ids is not None:
        row_ids = set(row_ids)
        for todo in data:
            uuid = todo["id"]
            done = todo["done"]
            if (uuid in row_ids and done is False) or (uuid not in row_ids and done is True):
                model.save_toggle_task(uuid)
                break
    return tab_name


Controller(
    output=Output(component_id="Tabs", component_property="value"),
    inputs=[Input(component_id="Table", component_property="selected_row_ids")],
    state=[
        State(component_id="Table", component_property="data"),
        State(component_id="Tabs", component_property="value"),
    ],
    func=toggle_todo,
)


def add_todo(_, name, date, description):
    """Обрабатывает добавление ToDo.

    Стирает информацию в диалоге и обнавляет отбражение данных.
    """
    if name is not None:
        model.save_task(name, date, description)
    return "", date, "", "ДОБАВИТЬ"


Controller(
    output=[
        Output(component_id="Name", component_property="value"),
        Output(component_id="Date", component_property="date"),
        Output(component_id="Description", component_property="value"),
        Output(component_id="Button", component_property="children"),
    ],
    inputs=[Input(component_id="Button", component_property="n_clicks")],
    state=[
        State(component_id="Name", component_property="value"),
        State(component_id="Date", component_property="date"),
        State(component_id="Description", component_property="value"),
    ],
    func=add_todo,
)


def activate_all(dash: Dash) -> NoReturn:
    """Активирует все контролерры для указанного Dash-приложения."""
    for controller in CONTROLLERS:
        kwargs = controller.dict()
        func = kwargs.pop("func")
        dash.callback(**kwargs)(func)
