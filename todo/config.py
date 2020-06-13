"""Ключевые параметры по умолчанию."""
from pathlib import Path

DB_PATH = Path(__file__).parents[1] / "db" / "ToDo.db"
BACKEND_URL = "http://localhost"
BACKEND_PORT = 5001
FRONTEND_PORT = 8000
