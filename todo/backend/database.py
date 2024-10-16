"""Опирации записи и чтения базы даных."""
import datetime
import sqlite3
from pathlib import Path
from typing import List, Optional
from typing import NoReturn
from uuid import UUID

from todo import config
from todo.backend.schema import ToDo


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
        if not Path(config.DB_PATH).exists():
            Path(config.DB_PATH).parent.mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(config.DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute(self._load_schema())

            cursor.execute('''
                CREATE TRIGGER IF NOT EXISTS update_zero_name
                AFTER INSERT ON Tasks
                BEGIN
                    UPDATE Tasks SET name = 'Задача' WHERE uuid = NEW.uuid AND (name IS NULL OR name = '');
                END;
            ''')

            conn.commit()
            self._conn = conn
        else:
            self._conn = sqlite3.connect(config.DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)

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


def search(name: str, description: str, date: Optional[datetime.date]) -> List[ToDo]:
    """Поиск дел по входным параметрам."""
    conn = get_conn()
    name_like = name + "%"
    description_like = description + "%"
    if date is None:
        res = conn.execute("SELECT * FROM Tasks WHERE name LIKE ? AND description LIKE ?", (name_like,description_like)).fetchall()
    else:
        res = conn.execute("SELECT * FROM Tasks WHERE name LIKE ? AND description LIKE ? AND DATE = ?", (name_like,description_like, date)).fetchall()
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


def toggle_task(uuid: UUID) -> NoReturn:
    """Переключает флаг завершенности дела."""
    conn = get_conn()
    conn.create_function("switch_done", 1, switch_done)
    done, *_ = conn.execute("SELECT switch_done(done) FROM Tasks WHERE uuid = ?", (uuid,)).fetchone()
    conn.execute("UPDATE Tasks SET done = ? WHERE uuid = ?", (done, uuid))
    conn.commit()


def switch_done(done: int) -> int:
    return not done


def add_task(todo: ToDo) -> NoReturn:
    """Добавить новое задание."""
    conn = get_conn()
    conn.execute("INSERT INTO Tasks VALUES (?,?,?,?,?)", todo.to_list())
    conn.commit()


def delete_all() -> NoReturn:
    """Очистить Базу данных"""
    conn = get_conn()
    conn.execute("DELETE FROM Tasks")
    conn.commit()
