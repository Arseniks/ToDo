from todo.backend import database


def test_get_all(tasks):
    assert tasks == database.get_all()


def test_get_overdue_tasks(tasks):
    assert tasks[3:4] == database.get_overdue_tasks()


def test_get_today_tasks(tasks):
    assert tasks[0:1] == database.get_today_tasks()


def test_get_pending_tasks(tasks):
    assert tasks[5:6] == database.get_pending_tasks()


def test_toggle_task(tasks):
    assert tasks[5:6] == database.get_pending_tasks()
    database.toggle_task(tasks[5].uuid)
    assert [] == database.get_pending_tasks()
    database.toggle_task(tasks[5].uuid)
    assert tasks[5:6] == database.get_pending_tasks()


def test_reopen_db(tasks, monkeypatch):
    assert tasks == database.get_all()
    monkeypatch.setattr(database.get_conn, "_conn", None)
    print(database.get_all()[0].to_list())
    assert tasks == database.get_all()
