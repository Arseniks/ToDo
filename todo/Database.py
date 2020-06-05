import sqlite3
import datetime
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, NoReturn, List
import os


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
    if not os.path.exists(DB_PATH):
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE Tasks
                          (id_ integer, name text, description text,
                           date real, done integer)
                       """)
        conn.commit()


def write(todo: ToDo) -> NoReturn:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Tasks VALUES (?,?,?,?,?)", (todo.id_, todo.name, todo.description, todo.date, todo.done))
        conn.commit()


def get_all() -> List:
    conn = get_conn()
    cursor = conn.cursor()
    res = cursor.execute("SELECT * FROM Tasks").fetchall()
    return res


def change_status(id_: int, new_status: int) -> NoReturn:
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
                UPDATE Tasks 
                SET done = ? 
                WHERE id_ = ?
                """, (new_status, id_))
    conn.commit()


def get_status(id_: int) -> str:
    conn = get_conn()
    cursor = conn.cursor()
    res = cursor.execute("SELECT done FROM Tasks WHERE id_ = ?", (id_, )).fetchall()
    res = res[0][0]
    return res


def get_today_tasks() -> List:
    today = datetime.date.today()
    conn = get_conn()
    cursor = conn.cursor()
    res = cursor.execute("SELECT * FROM Tasks WHERE date = ?", (today, )).fetchall()
    return res


def get_overdue_tasks() -> List:
    today = datetime.date.today()
    conn = get_conn()
    cursor = conn.cursor()
    res = cursor.execute("SELECT * FROM Tasks WHERE date < ?", (today, )).fetchall()
    return res
