"""Маленькое Web приложение по управлению ToDo."""
import argparse
from pathlib import Path

import dash
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

from todo import config
from todo.backend.endpoints import router
from todo.frontend import controller
from todo.frontend import view


def main():
    parser = argparse.ArgumentParser(prog="todo", description="Small Web App for ToDo")
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
    config.BACKEND_URL_WITH_PORT = f"{config.BACKEND_URL}:{args.port}"

    app_dash = dash.Dash(__name__, assets_folder="frontend/assets")
    app_dash.config.suppress_callback_exceptions = True
    app_dash.layout = view.TaskManager()
    controller.activate_all(app_dash)

    app = FastAPI()
    app.include_router(router)
    app.mount("/", WSGIMiddleware(app_dash.server))

    uvicorn.run(app, host="0.0.0.0", port=args.port, log_level="info")


if __name__ == "__main__":
    main()
