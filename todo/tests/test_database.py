from todo import database
from datetime import timedelta, date
import pytest
from uuid import uuid1


def get_today_date():
    today = date.today()
    return today


def get_tomorrow_date():
    tomorrow = get_today_date() + timedelta(days=1)
    return tomorrow


def get_yesterday_date():
    yesterday = get_today_date() - timedelta(days=1)
    return yesterday


def test():
    task1 = database.ToDo(uuid1(), 'Собраться в школу', get_today_date(), False, 'Собрать еду и рюкзак')
    task2 = database.ToDo(uuid1(), 'Сходить в магазин', get_today_date(), True, 'Купить воду и сок')
    task3 = database.ToDo(uuid1(), 'Собраться в школу', get_yesterday_date(), True, 'Собрать еду и рюкзак')
    task4 = database.ToDo(uuid1(), 'Сходить в магазин', get_yesterday_date(), False, 'Купить тортик')
    task5 = database.ToDo(uuid1(), 'Сделать дз', get_tomorrow_date(), True, 'Математика и английский')
    task6 = database.ToDo(uuid1(), 'Сходить в аптеку', get_tomorrow_date(), False, 'Капли дляя носа')
    database.add_task(task1)
    database.add_task(task2)
    database.add_task(task3)
    database.add_task(task4)
    database.add_task(task5)
    database.add_task(task6)
    assert [task1] == database.get_today_tasks()
    assert [task1, task2, task3, task4, task5, task6] == database.get_all()
    assert [task4] == database.get_overdue_tasks()
    assert [task6] == database.get_pending_tasks()
    database.complete_task(task6.uuid)
    assert [task6] != database.get_pending_tasks()









