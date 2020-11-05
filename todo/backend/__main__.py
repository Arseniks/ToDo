"""REST API сервис для управления ToDo на базе fastapi, pydantic и SQLite."""
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from todo.backend.config import PORT
from todo.backend.endpoints import router

import json

app = FastAPI()

conf = open("./ToDo/todo/frontend/react-intro/src/config.json", "r")
data = json.load(conf)["frontend"]

origins = [
    "http://" + data["host"] + ":" + str(data["port"]),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def main():
    app.include_router(router)
    uvicorn.run(f"{Path(__name__)}:app", host="0.0.0.0", port=PORT, log_level="info")


if __name__ == "__main__":
    main()
