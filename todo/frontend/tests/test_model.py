from datetime import date, timedelta

from todo.frontend import model


def get_today_date():
    today = date.today()
    return today


def get_tomorrow_date():
    tomorrow = get_today_date() + timedelta(days=1)
    return tomorrow


def get_yesterday_date():
    yesterday = get_today_date() - timedelta(days=1)
    return yesterday


DATA = [{'name': 'Собраться в школу', 'date': get_yesterday_date(), 'done': True, 'description': 'Собрать еду и рюкзак',
         'id': 'fe6cd177-a8da-11ea-abfc-d46d6da674b6'},
        {'name': 'Сходить в магазин', 'date': get_yesterday_date(), 'done': False, 'description': 'Купить воду и сок',
         'id': 'fe6cd178-a8da-11ea-a391-d46d6da674b6'},
        {'name': 'Собраться в школу', 'date': get_today_date(), 'done': True, 'description': 'Собрать еду и рюкзак',
         'id': 'fe6cd179-a8da-11ea-af26-d46d6da674b6'},
        {'name': 'Сходить в магазин', 'date': get_today_date(), 'done': False, 'description': 'Купить тортик',
         'id': 'fe6cd17a-a8da-11ea-8c91-d46d6da674b6'},
        {'name': 'Сделать дз', 'date': get_tomorrow_date(), 'done': True, 'description': 'Математика и английский',
         'id': 'fe6cd17b-a8da-11ea-8a55-d46d6da674b6'},
        {'name': 'Сходить в аптеку', 'date': get_tomorrow_date(), 'done': False, 'description': 'Капли для носа',
         'id': 'fe6cd17c-a8da-11ea-93a1-d46d6da674b6'}]

SELECTED_ROWS = [0, 2, 4]


def test_make_url():
    assert model.make_url("toggle/") == 'http://localhost:5001/toggle/'
