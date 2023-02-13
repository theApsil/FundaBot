import sqlite3
import os
from dataclasses import dataclass

DB_NAME = "tasks.db"
TASK_TABLE_NAME = "task"


@dataclass
class Task:
    task_id: int
    user_id: int
    task_name: str
    task_description: str
    completion_flag: bool
    payment_flag: bool


con = sqlite3.connect(DB_NAME, check_same_thread=False)
sql = con.cursor()

sql.execute(f"""
    CREATE TABLE IF NOT EXISTS {TASK_TABLE_NAME}
    (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        task_name TEXT,
        task_description TEXT,
        completion_flag BOOL,
        payment_flag BOOL
    ) 
""")
con.commit()


def get_task(task_id: int) -> Task:
    sql.execute(f"""
        SELECT * 
        FROM {TASK_TABLE_NAME}
        WHERE task_id = ? 
    """, (task_id,))
    row = sql.fetchone()
    return Task(*row)


def create_task(user_id: int, task_name: str, task_description: str) -> None:
    sql.execute(f"""
        INSERT INTO {TASK_TABLE_NAME} (user_id, task_name, task_description, completion_flag, payment_flag)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, task_name, task_description, False, False))
    con.commit()


def get_all_tasks() -> list[Task]:
    sql.execute(f"""
        SELECT *
        FROM {TASK_TABLE_NAME}
    """)
    rows = sql.fetchall()
    tasks = []
    for row in rows:
        task = Task(*row)
        tasks.append(task)
    return tasks


def get_uncompleted_tasks() -> list[Task]:
    sql.execute(f"""
        SELECT *
        FROM {TASK_TABLE_NAME}
        WHERE completion_flag = ?
    """, (False,))
    rows = sql.fetchall()
    tasks = []
    for row in rows:
        task = Task(*row)
        tasks.append(task)
    return tasks


def mark_task_completed(task_id: int) -> None:
    sql.execute(f"""
        UPDATE {TASK_TABLE_NAME}
        SET completion_flag = ?
        WHERE task_id = ?
    """, (task_id,))
    con.commit()
