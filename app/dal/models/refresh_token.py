from sqlalchemy import UUID, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped
from uuid import uuid4
from .user import User
from .base import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[str] = mapped_column(UUID(), primary_key=True, default=uuid4)
    expires_in: Mapped[int] = mapped_column(Integer())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship()

    def __repr__(self) -> str:
        return f"RefreshToken(id={self.id!r}, expires_at={self.expires_in!r}, user_id={self.user_id!r}, {self.ts_repr()})"
