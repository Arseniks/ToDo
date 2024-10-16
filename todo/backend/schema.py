"""Схемы данных ответов и запросов."""
import datetime
from typing import Any
from typing import List
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ToDo(BaseModel):
    uuid: UUID
    name: str
    date: datetime.date
    done: bool
    description: Optional[str] = None

    @classmethod
    def from_list(cls, *args):
        """Конструктор из списка значений."""
        return cls(**{name: value for name, value in zip(cls.__fields__, args)})

    def to_list(self) -> List[Any]:
        """Преобразовать в список значений полей."""
        return [value for _, value in self]

class SearchData(BaseModel):
    name: str
    date:  Optional[datetime.date] = None
    description: Optional[str] = None

class Uuid(BaseModel):
    uuid: UUID
