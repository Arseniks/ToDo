import sqlite3
import datetime
from pathlib import Path
from typing import Optional, NoReturn


DB_PATH = Path("ToDo.db")
CONNECTION = sqlite3.connect(DB_PATH)


def get_conn() -> sqlite3.Connection:
    return CONNECTION


def create_database() -> NoReturn:
    # Проверить, что база существует
    try:
        conn = sqlite3.connect("ToDo.db")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE Tasks
                          (id_ integer, name text, description text,
                           date real, done integer)
                       """)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])


def write(id_: int, name: str, date: datetime.date,  done: int, description: Optional[str] = None) -> NoReturn:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Tasks VALUES (?,?,?,?,?)", (id_, name, description, date, done))
        conn.commit()


def get_all():
    try:
        conn = sqlite3.connect("ToDo.db")
        cursor = conn.cursor()
        res = cursor.execute("SELECT * FROM Tasks").fetchall()
        conn.close()
        return res
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])


def change_status(id_, new_status):
    try:
        conn = sqlite3.connect("ToDo.db")
        cursor = conn.cursor()
        cursor.execute("""
                    UPDATE Tasks 
                    SET done = ? 
                    WHERE id_ = ?
                    """, (new_status, id_))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])


def get_status(id_):
    try:
        conn = sqlite3.connect("ToDo.db")
        cursor = conn.cursor()
        res = cursor.execute("SELECT done FROM Tasks WHERE id_ = ?", (id_, )).fetchall()
        res = res[0][0]
        conn.close()
        return res
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])


def get_today_tasks():
    today = datetime.date.today()
    try:
        conn = sqlite3.connect("ToDo.db")
        cursor = conn.cursor()
        res = cursor.execute("SELECT * FROM Tasks WHERE date = ?", (today, )).fetchall()
        conn.close()
        return res
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])


def get_overdue_tasks():
    today = datetime.date.today()
    try:
        conn = sqlite3.connect("ToDo.db")
        cursor = conn.cursor()
        res = cursor.execute("SELECT * FROM Tasks WHERE date < ?", (today, )).fetchall()
        conn.close()
        return res
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])

