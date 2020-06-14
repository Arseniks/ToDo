"""Frontend для управления ToDo с использованием подхода Model-View-Controller на базе Dash."""
import argparse

import dash
import uvicorn

from todo import config
from todo.frontend import controller
from todo.frontend import view


def main():
    # Добавить запрос двух параметров с дефолтными значенимими:
    # - server - f"{config.BACKEND_URL}:{config.BACKEND_PORT}/"
    # - port - config.FRONTEND_PORT,
    parser = argparse.ArgumentParser(prog="todo.frontend", description="dash client for ToDo")
    parser.add_argument(
        "--server",
        default=f"{config.BACKEND_URL}:{config.BACKEND_PORT}/",
        type=str,
        help=f"backend server address with port [default: {config.DB_PATH}]",
    )
    parser.add_argument(
        "--port",
        default=config.FRONTEND_PORT,
        type=int,
        help=f"frontend port [default: {config.FRONTEND_PORT}]",
    )
    args = parser.parse_args()
    app = dash.Dash(__name__)
    app.config.suppress_callback_exceptions = True
    app.layout = view.TaskManager()
    controller.activate_all(app)
    uvicorn.run(app.server, host="0.0.0.0", port=args.port, interface="wsgi")


if __name__ == "__main__":
    main()
