from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255))
    password_hash: Mapped[str] = mapped_column(String(64))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.username!r}, password_hash={self.password_hash!r})"
