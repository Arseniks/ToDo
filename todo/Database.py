import sqlite3
import datetime


def create_database():
    try:
        conn = sqlite3.connect("ToDo.db")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE Tasks
                          (number integer, name text, description text,
                           date real, done text)
                       """)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])


def write(number, name, description, date, done='-'):
    try:
        conn = sqlite3.connect("ToDo.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Tasks VALUES (?,?,?,?,?)", (number, name, description, date, done))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])


def get_all():
    try:
        conn = sqlite3.connect("ToDo.db")
        cursor = conn.cursor()
        res = cursor.execute("SELECT * FROM Tasks").fetchall()
        conn.close()
        return res
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])


def change_status(number, new_status):
    try:
        conn = sqlite3.connect("ToDo.db")
        cursor = conn.cursor()
        cursor.execute("""
                    UPDATE Tasks 
                    SET done = ? 
                    WHERE number = ?
                    """, (new_status, number))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])


def get_status(number):
    try:
        conn = sqlite3.connect("ToDo.db")
        cursor = conn.cursor()
        res = cursor.execute("SELECT done FROM Tasks WHERE number = ?", (number, )).fetchall()
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

