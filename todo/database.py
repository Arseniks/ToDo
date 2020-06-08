"""Опирации записи и чтения базы даных."""
import datetime
import sqlite3
from pathlib import Path
from typing import Optional, NoReturn, List, Any
from uuid import UUID

from pydantic import BaseModel

DB_PATH = Path("ToDo.db")


class ToDo(BaseModel):
    uuid: UUID
    name: str
    date: datetime.date
    done: bool
    description: Optional[str] = None

    @classmethod
    def from_list(cls, *args):
        """Конструктор из списка значений."""
        return cls(**{name: value for name, value in zip(cls.__fields__, args)})

    def to_list(self) -> List[Any]:
        """Преобразовать в список значений полей."""
        return [value for _, value in self]


class DBConnector:
    def __init__(self):
        sqlite3.register_adapter(bool, int)
        sqlite3.register_converter("bool", lambda x: bool(int(x.decode())))

        sqlite3.register_adapter(UUID, str)
        sqlite3.register_converter("uuid", lambda x: UUID(x.decode()))

        self._conn = None

    @staticmethod
    def _load_schema() -> str:
        path = Path(__file__).parent / "make_db.sql"
        with open(path, "r") as f:
            return f.read()

    def _create_conn(self) -> NoReturn:
        if not Path(DB_PATH).exists():
            conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
            cursor = conn.cursor()
            cursor.execute(self._load_schema())
            conn.commit()
            self._conn = conn
        else:
            self._conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)

    def __call__(self) -> sqlite3.Connection:
        if self._conn is None:
            self._create_conn()
        return self._conn


get_conn = DBConnector()


def get_all() -> List[ToDo]:
    """Получение всех дел."""
    conn = get_conn()
    res = conn.execute("SELECT * FROM Tasks").fetchall()
    return [ToDo.from_list(*todo) for todo in res]


def get_overdue_tasks() -> List[ToDo]:
    """Список дел просроченных и не законченых дел."""
    today = datetime.date.today()
    conn = get_conn()
    res = conn.execute("SELECT * FROM Tasks WHERE date < ? AND done = 0", (today,)).fetchall()
    return [ToDo.from_list(*todo) for todo in res]


def get_today_tasks() -> List[ToDo]:
    """Список дел с окончанием сегодня и не законченых."""
    today = datetime.date.today()
    conn = get_conn()
    res = conn.execute("SELECT * FROM Tasks WHERE date = ? AND done = 0", (today,)).fetchall()
    return [ToDo.from_list(*todo) for todo in res]


def get_pending_tasks() -> List[ToDo]:
    """Список дел с окончанием в будущем и не законченых."""
    today = datetime.date.today()
    conn = get_conn()
    res = conn.execute("SELECT * FROM Tasks WHERE date > ? AND done = 0", (today,)).fetchall()
    return [ToDo.from_list(*todo) for todo in res]


def add_task(todo: ToDo) -> NoReturn:
    """Добавить новое задание."""
    conn = get_conn()
    conn.execute("INSERT INTO Tasks VALUES (?,?,?,?,?)", todo.to_list())
    conn.commit()


def toggle_task(uuid: UUID) -> NoReturn:
    """Переключает флаг завершенности дела."""
    conn = get_conn()
    done, *_ = conn.execute("SELECT done FROM Tasks WHERE uuid = ?", (uuid,)).fetchone()
    print(done)
    done = not done
    print(done)
    conn.execute("UPDATE Tasks SET done = ? WHERE uuid = ?", (done, uuid))
    conn.commit()
