# ToDo
[![Tests](https://github.com/Arseniks/ToDo/workflows/Tests/badge.svg)](https://github.com/Arseniks/ToDo/actions)
[![codecov](https://codecov.io/gh/Arseniks/ToDo/branch/master/graph/badge.svg)](https://codecov.io/gh/Arseniks/ToDo)
[![Updates](https://pyup.io/repos/github/Arseniks/ToDo/shield.svg)](https://pyup.io/repos/github/Arseniks/ToDo/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Маленькое Web приложение по управлению ToDo:
 - Backend - REST сервис на базе FastAPI, pydantic и SQLite
 - Frontend - Dash приложение с использованием паттерна Model-View-Controller
 - Запуск с помощью ASGI сервера Uvicorn

## Запуск всего приложения

    todo [-h] [--db_path DB_PATH] [--port PORT]

    Small Web App for ToDo
    
    Dash app at \ 
    REST API docs at \docs\ 
    
    optional arguments:
      -h, --help         show this help message and exit
      --db_path DB_PATH  path and file name of QSLite database [default: db/ToDo.db]
      --port PORT        bind socket to this port [default: 5001]


## Запуск REST сервиса

    todo.backend [-h] [--db_path DB_PATH] [--port PORT]

    REST server for ToDo - API docs at \docs\
    
    optional arguments:
      -h, --help         show this help message and exit
      --db_path DB_PATH  path and file name of QSLite database [default: db/ToDo.db]
      --port PORT        bind socket to this port [default: 5001]

## Запуск Dash приложения

    todo.frontend [-h] [--server SERVER] [--port PORT]
    
    Dash client for ToDo
    
    optional arguments:
      -h, --help       show this help message and exit
      --server SERVER  backend server address with port [default: http://localhost:5001]
      --port PORT      bind socket to this port [default: 8000]
