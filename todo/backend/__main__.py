"""REST API сервис для управления ToDo на базе fastapi, pydantic и SQLite."""
import argparse
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from todo.backend.config import PORT
from todo.backend.endpoints import router

app = FastAPI()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default=Path(__name__), type=str)
    parser.add_argument('--port', default=PORT, type=int)
    args = parser.parse_args()

    app.include_router(router)
    uvicorn.run(f"{args.path}:app", host="0.0.0.0", port=args.port, log_level="info")


if __name__ == "__main__":
    main()
