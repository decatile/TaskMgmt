from typing import Any, Protocol
from sqlalchemy.orm import Mapped


class Entity(Protocol):
    id: Mapped[Any]
