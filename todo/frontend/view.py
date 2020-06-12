import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt


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
        return [
            {name: value for name, value in zip(["id"] + self.columns(), i[1:])} for i in self.overdue()
        ]

    def data_today(self):
        return [
            {name: value for name, value in zip(["id"] + self.columns(), i[1:])} for i in self.today()
        ]

    def data_pending(self):
        return [
            {name: value for name, value in zip(["id"] + self.columns(), i[1:])} for i in self.pending()
        ]

    def data_all(self):
        return [{name: value for name, value in zip(["id"] + self.columns(), i[1:])} for i in self.all()]


class TaskManager(html.Div):
    """HTML представление приложения по управлению ToDO."""

    def __init__(self):
        data = Data()
        tabs = [
            TableTab("Today", data.data_today(), data.today()),
            TableTab("Overdue", data.data_overdue(), data.overdue()),
            TableTab("Pending", data.data_pending(), data.pending()),
            TableTab("All", data.data_all(), data.all()),
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

    def __init__(self, name, data, selected):
        table = dt.DataTable(
            id=f"T_{name.lower()}",
            columns=[
                {"name": "Name", "id": "Name", "type": "text"},
                {"name": "Date", "id": "Date", "type": "datetime"},
                {"name": "Description", "id": "Description", "Description": "text"},
            ],
            data=data,
            editable=True,
            sort_action="native",
            row_selectable="multi",
            selected_rows=selected,
            style_cell={"textAlign": "left", "whiteSpace": "normal"},
            style_table={"overflowY": "auto", "marginLeft": 6},
            style_as_list_view=True,
        )
        super().__init__(
            label=name, value=name, children=[table],
        )


class Dialog(html.Div):
    """Диалог для ввода нового ToDO."""

    def __init__(self):
        super().__init__(
            children=[
                html.H2("Add task"),
                dcc.Input(style={"marginTop": 0}, placeholder="Name"),
                dcc.DatePickerSingle(display_format="YYYY-MM-DD"),
                dcc.Textarea(placeholder="Description", style={"height": 100}),
                html.Button(children="ADD", id="button"),
            ],
            style={"display": "flex", "flexFlow": "column wrap", "maxWidth": 480},
        )
