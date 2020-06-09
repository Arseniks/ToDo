"""REST API сервис для управления ToDo на базе fastapi, pydantic и SQLite."""
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from todo.backend.config import PORT
from todo.backend.endpoints import router

app = FastAPI()


def main():
    app.include_router(router)
    uvicorn.run(f"{Path(__name__)}:app", host="0.0.0.0", port=PORT, log_level="info")


if __name__ == "__main__":
    main()
