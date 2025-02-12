from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped
from uuid import uuid4
from .user import User
from .base import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[UUID] = mapped_column(UUID(), primary_key=True, default=uuid4)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship()

    def __repr__(self) -> str:
        return (
            f"RefreshToken(id={self.id!r}, user_id={self.user_id!r}, {self.ts_repr()})"
        )
