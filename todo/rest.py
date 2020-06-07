from fastapi import FastAPI

from todo import database

app = FastAPI()


@app.get("/overdue")
async def overdue():
    return database.get_overdue_tasks()


@app.get("/today")
async def today():
    return database.get_today_tasks()


@app.get("/pending")
async def pending():
    return database.get_pending_tasks()


@app.post("/add/")
async def create_todo(todo: database.ToDo):
    database.add_task(todo)


@app.patch("/complete")
async def patch_todo(uuid: database.UUID):
    database.complete_task(uuid)
