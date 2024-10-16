"""End points for REST API."""
from typing import List

from fastapi import APIRouter, Query

from todo.backend import database
from todo.backend.schema import ToDo, SearchData
from todo.backend.schema import Uuid

router = APIRouter()


@router.get("/all/", response_model=List[ToDo])
async def all_():
    """Получение всех дел."""
    return database.get_all()

@router.post("/search/", response_model=List[ToDo])
async def search_(search_data: SearchData):
    """Список дел по входным параметрам."""
    return database.search(search_data.name, search_data.description, search_data.date)


@router.get("/overdue/", response_model=List[ToDo])
async def overdue():
    """Список дел просроченных и не законченых дел."""
    return database.get_overdue_tasks()


@router.get("/today/", response_model=List[ToDo])
async def today():
    """Список дел с окончанием сегодня и не законченых."""
    return database.get_today_tasks()


@router.get("/pending/", response_model=List[ToDo])
async def pending():
    """Список дел с окончанием в будущем и не законченых."""
    return database.get_pending_tasks()


@router.patch("/toggle/")
async def toggle_task(uuid: Uuid):
    """Переключает флаг завершенности дела."""
    database.toggle_task(uuid.uuid)


@router.post("/add/")
async def create_task(todo: ToDo):
    """Добавить новое задание."""
    database.add_task(todo)
