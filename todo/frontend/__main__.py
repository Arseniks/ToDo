"""Frontend для управления ToDo с использованием подхода Model-View-Controller на базе Dash."""
import dash
import uvicorn

from todo import config
from todo.frontend import controller
from todo.frontend import view


def main():
    # Добавить запрос двух параметров с дефолтными значенимими:
    # - server - f"{config.BACKEND_URL}:{config.BACKEND_PORT}/"
    # - port - config.FRONTEND_PORT,
    app = dash.Dash(__name__)
    app.config.suppress_callback_exceptions = True
    app.layout = view.TaskManager()
    controller.activate_all(app)
    uvicorn.run(app.server, host="0.0.0.0", port=config.FRONTEND_PORT, interface="wsgi")


if __name__ == "__main__":
    main()
