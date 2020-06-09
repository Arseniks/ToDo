"""REST API сервис для управления ToDo на базе fastapi, pydantic и SQLite."""
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from backend.config import PORT
from backend.endpoints import router

app = FastAPI()


def main():
    app.include_router(router)
    uvicorn.run(f"{Path(__name__)}:app", host="0.0.0.0", port=PORT, log_level="info")


if __name__ == "__main__":
    main()
