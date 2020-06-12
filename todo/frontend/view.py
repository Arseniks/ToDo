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


class Tab:
    def __init__(self, name, data_):
        self.name = name
        self.data = data_

    def get_table(self):
        return dt.DataTable(
            id=f"T_{self.name.lower()}",
            columns=[{"name": col, "id": col, "type": types} for n, (col, types) in
                     enumerate(zip(data.columns(), data.types()))],
            data=self.data,
            editable=True,
            sort_action="native",
            row_selectable="multi",
            selected_rows=[n for n, i in enumerate(data.today()) if i[0]],
            style_cell={"textAlign": "left", "whiteSpace": "normal"},
            style_table={"overflowY": "auto", "marginLeft": 6},
            style_as_list_view=True,
        )

    def get_tab(self):
        return dcc.Tab(label=self.name, value=self.name, children=[self.get_table()], )


class Dialog(html.Div):
    def __init__(self, children, style):
        super().__init__()
        self.children = children
        self.style = style


def main_html():
    app.layout = html.Div(
        [html.H1("Tasks manager"), dcc.Tabs(id="tabs", value="All", vertical=True, children=get_tabs()),
         Dialog(children=[
             html.H6('Add task'),
             dcc.Input(style={'marginTop': 0}, placeholder='Name'),
             dcc.DatePickerSingle(display_format='YYYY-MM-DD'),
             dcc.Textarea(placeholder='Description', style={'height': 100}),
             html.Button(children='ADD', id='button')],
             style={'display': 'flex', 'flexFlow': 'column wrap', 'maxWidth': 480})])

def get_tabs():
    today = Tab('Today', data.data_today())
    today_tab = today.get_tab()
    overdue = Tab('Overdue', data.data_overdue())
    overdue_tab = overdue.get_tab()
    pending = Tab('Pending', data.data_pending())
    pending_tab = pending.get_tab()
    all_ = Tab('All', data.data_all())
    all_tab = all_.get_tab()
    return [
        today_tab,
        overdue_tab,
        pending_tab,
        all_tab
    ]


if __name__ == "__main__":
    app = dash.Dash(__name__)
    data = Data()
    main_html()
    uvicorn.run(f"{__name__}:app.server", interface="wsgi", host="0.0.0.0")
