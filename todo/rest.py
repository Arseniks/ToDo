"""End points for REST API."""
from typing import List
from uuid import UUID

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from todo import database
from todo.database import ToDo


class Uuid(BaseModel):
    uuid: UUID


app = FastAPI()


@app.get("/all/")
async def all_() -> List[ToDo]:
    """Получение всех дел."""
    return database.get_all()


@app.get("/overdue/")
async def overdue() -> List[ToDo]:
    """Список дел просроченных и не законченых дел."""
    return database.get_overdue_tasks()


@app.get("/today/")
async def today() -> List[ToDo]:
    """Список дел с окончанием сегодня и не законченых."""
    return database.get_today_tasks()


@app.get("/pending/")
async def pending() -> List[ToDo]:
    """Список дел с окончанием в будущем и не законченых."""
    return database.get_pending_tasks()


@app.post("/add/")
async def create_task(todo: ToDo):
    """Добавить новое задание."""
    database.add_task(todo)


@app.patch("/complete/")
async def toggle_task(uuid: Uuid):
    """Переключает флаг завершенности дела."""
    database.toggle_task(uuid.uuid)


if __name__ == "__main__":
    uvicorn.run("rest:app", host="127.0.0.1", port=5000, log_level="info")
