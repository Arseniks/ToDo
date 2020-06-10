import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import uvicorn


class Data:
    def __init__(self):
        self.task0 = [False, "a", "Собраться в школу", "2020-06-08", "Собрать еду и рюкзак"]
        self.task1 = [True, "b", "Сходить в магазин", "2020-06-08", "Купить воду и сок"]
        self.task2 = [True, "c", "Собраться в школу", "2020-06-07", "Собрать еду и рюкзак"]
        self.task3 = [False, "d", "Сходить в магазин", "2020-06-07", "Купить тортик"]
        self.task4 = [True, "e", "Сделать дз", "2020-06-09", "Математика и английский"]
        self.task5 = [False, "f", "Сходить в аптеку", "2020-06-09", "Капли дляя носа"]

    @staticmethod
    def columns():
        return ["Name", "Date", "Description"]

    @staticmethod
    def types():
        return ["text", "datetime", "text"]

    def overdue(self):
        return [self.task1]

    def today(self):
        return [self.task2]

    def pending(self):
        return [self.task4]

    def all(self):
        return [self.task0, self.task1, self.task2, self.task3, self.task4, self.task5]

    def data_overdue(self):
        return [{name: value for name, value in zip(["id"] + self.columns(), i[1:])} for i in self.overdue()]

    def data_today(self):
        return [{name: value for name, value in zip(["id"] + self.columns(), i[1:])} for i in self.today()]

    def data_pending(self):
        return [{name: value for name, value in zip(["id"] + self.columns(), i[1:])} for i in self.pending()]

    def data_all(self):
        return [{name: value for name, value in zip(["id"] + self.columns(), i[1:])} for i in self.all()]


def main_html():
    app.layout = html.Div(
        [html.H1("Tasks manager"), dcc.Tabs(id="tabs", value="All", vertical=True, children=get_tabs()), ])


def get_tabs():
    return [
        get_today_tab(),
        get_overdue_tab(),
        get_pending_tab(),
        get_all_tab()
    ]


def get_today_tab():
    return dcc.Tab(label="Today", value="Today", children=[get_today_table(), *get_dialog_today()], )


def get_overdue_tab():
    return dcc.Tab(label="Overdue", value="Overdue", children=[get_overdue_table(), *get_dialog_overdue()], )


def get_pending_tab():
    return dcc.Tab(label="Pending", value="Pending", children=[get_pending_table(), *get_dialog_pending()], )


def get_all_tab():
    return dcc.Tab(label="All", value="All", children=[get_all_table(), *get_dialog_all()], )


def get_today_table():
    return dt.DataTable(
        id="T_today",
        columns=[{"name": col, "id": col, "type": types} for n, (col, types) in
                 enumerate(zip(data.columns(), data.types()))],
        data=data.data_today(),
        editable=True,
        sort_action="native",
        row_selectable="multi",
        selected_rows=[n for n, i in enumerate(data.today()) if i[0]],
        style_cell={"textAlign": "left", "whiteSpace": "normal", "maxWidth": 400},
        style_table={"overflowY": "auto"},
    )


def get_overdue_table():
    return dt.DataTable(
        id="T_overdue",
        columns=[{"name": col, "id": col, "type": types} for n, (col, types) in
                 enumerate(zip(data.columns(), data.types()))],
        data=data.data_overdue(),
        editable=True,
        sort_action="native",
        row_selectable="multi",
        selected_rows=[n for n, i in enumerate(data.overdue()) if i[0]],
        style_cell={"textAlign": "left", "whiteSpace": "normal", "maxWidth": 400},
        style_table={"overflowY": "auto"},
    )


def get_pending_table():
    return dt.DataTable(
        id="T_pending",
        columns=[{"name": col, "id": col, "type": types} for n, (col, types) in
                 enumerate(zip(data.columns(), data.types()))],
        data=data.data_pending(),
        editable=True,
        sort_action="native",
        row_selectable="multi",
        selected_rows=[n for n, i in enumerate(data.pending()) if i[0]],
        style_cell={"textAlign": "left", "whiteSpace": "normal", "maxWidth": 400},
        style_table={"overflowY": "auto"},
    )


def get_all_table():
    return dt.DataTable(
        id="T_all",
        columns=[{"name": col, "id": col, "type": types} for n, (col, types) in
                 enumerate(zip(data.columns(), data.types()))],
        data=data.data_all(),
        editable=True,
        sort_action="native",
        row_selectable="multi",
        selected_rows=[n for n, i in enumerate(data.all()) if i[0]],
        style_cell={"textAlign": "left", "whiteSpace": "normal", "maxWidth": 400},
        style_table={"overflowY": "auto"},
    )


def get_dialog_all():
    return [
        dcc.Input(placeholder="Name"),
        dcc.Textarea(placeholder="Description", style={"height": 100}),
        dcc.DatePickerSingle(display_format="YYYY-MM-DD", style={"borderRadius": "4px"}),
        html.Button("ADD", id="button_all"),
    ]


def get_dialog_today():
    return [
        dcc.Input(placeholder="Name"),
        dcc.Textarea(placeholder="Description", style={"height": 100}),
        dcc.DatePickerSingle(display_format="YYYY-MM-DD", style={"borderRadius": "4px"}),
        html.Button("ADD", id="button_today"),
    ]


def get_dialog_pending():
    return [
        dcc.Input(placeholder="Name"),
        dcc.Textarea(placeholder="Description", style={"height": 100}),
        dcc.DatePickerSingle(display_format="YYYY-MM-DD", style={"borderRadius": "4px"}),
        html.Button("ADD", id="button_pending"),
    ]


def get_dialog_overdue():
    return [
        dcc.Input(placeholder="Name"),
        dcc.Textarea(placeholder="Description", style={"height": 100}),
        dcc.DatePickerSingle(display_format="YYYY-MM-DD", style={"borderRadius": "4px"}),
        html.Button("ADD", id="button_overdue"),
    ]


if __name__ == "__main__":
    app = dash.Dash(__name__)
    data = Data()
    main_html()
    uvicorn.run(f"{__name__}:app.server", interface="wsgi", host="0.0.0.0")
