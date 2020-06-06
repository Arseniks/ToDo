import sqlite3
import datetime
from dataclasses import dataclass, astuple
from pathlib import Path
from typing import Optional, NoReturn, List

from uuid import UUID

DB_PATH = Path("ToDo.db")


class DBConnector:
    def __init__(self):

        sqlite3.register_adapter(bool, int)
        sqlite3.register_converter("bool", bool)

        sqlite3.register_adapter(UUID, str)
        sqlite3.register_converter("uuid", UUID)

        if not Path(DB_PATH).exists():
            conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE Tasks
                                      (uuid uuid, name text,
                                       date date, done bool, description text)
                                   """)
            conn.commit()
            self._conn = conn
        else:
            self._conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)

    def __call__(self):
        return self._conn


get_conn = DBConnector()


@dataclass
class ToDo:
    uuid: UUID
    name: str
    date: datetime.date
    done: bool
    description: Optional[str] = None

    def to_db_record(self) -> tuple:
        return astuple(self)


def get_all() -> List[ToDo]:
    """Получение всех дел."""
    conn = get_conn()
    cursor = conn.cursor()
    res = cursor.execute("SELECT * FROM Tasks").fetchall()
    return [ToDo(*todo) for todo in res]


def get_overdue_tasks() -> List[ToDo]:
    """Список дел просроченных и не законченых дел."""
    today = datetime.date.today()
    conn = get_conn()
    cursor = conn.cursor()
    res = cursor.execute("SELECT * FROM Tasks WHERE date < ? AND done = 0", (today, )).fetchall()
    return [ToDo(*todo) for todo in res]


def get_today_tasks() -> List[ToDo]:
    """Список дел с окончанием сегодня и не законченых."""
    today = datetime.date.today()
    conn = get_conn()
    cursor = conn.cursor()
    res = cursor.execute("SELECT * FROM Tasks WHERE date = ? AND done = 0", (today, )).fetchall()
    return [ToDo(*todo) for todo in res]


def get_pending_tasks() -> List[ToDo]:
    """Список дел с окончанием в будущем и не законченых."""
    today = datetime.date.today()
    conn = get_conn()
    cursor = conn.cursor()
    res = cursor.execute("SELECT * FROM Tasks WHERE date > ? AND done = 0", (today, )).fetchall()
    return [ToDo(*todo) for todo in res]


def add_task(todo: ToDo) -> NoReturn:
    """Добавить новое задание."""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Tasks VALUES (?,?,?,?,?)", todo.to_db_record())
    conn.commit()


def complete_task(uuid: UUID) -> NoReturn:
    """Завершает дело."""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
                UPDATE Tasks 
                SET done = 1 
                WHERE id_ = ?
                """, (uuid, ))
    conn.commit()
