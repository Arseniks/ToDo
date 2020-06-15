"""REST API сервис для управления ToDo на базе fastapi, pydantic и SQLite."""
import argparse
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from todo import config
from todo.backend.endpoints import router


def main():
    description = "REST server for ToDo - API docs at \\docs\\"
    parser = argparse.ArgumentParser(prog="todo.backend", description=description, )
    parser.add_argument(
        "--db_path",
        default=config.DB_PATH,
        type=str,
        help=f"path and file name of QSLite database [default: {config.DB_PATH}]",
    )
    parser.add_argument(
        "--port",
        default=config.BACKEND_PORT,
        type=int,
        help=f"bind socket to this port [default: {config.BACKEND_PORT}]",
    )
    args = parser.parse_args()
    config.DB_PATH = Path(args.db_path)

    app = FastAPI()
    app.include_router(router)

    uvicorn.run(app, host="0.0.0.0", port=args.port, log_level="info")


if __name__ == "__main__":
    main()
