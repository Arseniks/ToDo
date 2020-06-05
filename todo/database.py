import sqlite3
import datetime
from dataclasses import dataclass, astuple
from pathlib import Path
from typing import Optional, NoReturn, List

DB_PATH = Path("ToDo.db")
CONNECTION = sqlite3.connect(DB_PATH)


def get_conn() -> sqlite3.Connection:
    return CONNECTION


@dataclass
class ToDo:
    id_: int
    name: str
    date: datetime.date
    done: int
    description: Optional[str] = None


def create_database() -> NoReturn:
    """Проверяет наличие и создает базу данных."""
    if not Path(DB_PATH).exists():
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE Tasks
                          (id_ integer, name text,
                           date real, done integer, description text)
                       """)
        conn.commit()


def write(todo: ToDo) -> NoReturn:
    """Сохранение в базу."""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Tasks VALUES (?,?,?,?,?)", astuple(todo))
    conn.commit()


def get_all() -> List[ToDo]:
    """Получение всех дел."""
    conn = get_conn()
    cursor = conn.cursor()
    res = cursor.execute("SELECT * FROM Tasks").fetchall()
    return [ToDo(*todo) for todo in res]


def change_status(id_: int, new_status: int) -> NoReturn:
    """Меняет статус выполнения дела."""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
                UPDATE Tasks 
                SET done = ? 
                WHERE id_ = ?
                """, (new_status, id_))
    conn.commit()


def get_status(id_: int) -> int:
    """Получить статус дела."""
    conn = get_conn()
    cursor = conn.cursor()
    res = cursor.execute("SELECT done FROM Tasks WHERE id_ = ?", (id_, )).fetchall()
    res = res[0][0]
    return res


def get_today_tasks() -> List[ToDo]:
    """Список дел с окончанием сегодня."""
    today = datetime.date.today()
    conn = get_conn()
    cursor = conn.cursor()
    res = cursor.execute("SELECT * FROM Tasks WHERE date = ?", (today, )).fetchall()
    return [ToDo(*todo) for todo in res]


def get_overdue_tasks() -> List[ToDo]:
    """Список дел просроченных дел."""
    today = datetime.date.today()
    conn = get_conn()
    cursor = conn.cursor()
    res = cursor.execute("SELECT * FROM Tasks WHERE date < ?", (today, )).fetchall()
    return [ToDo(*todo) for todo in res]
