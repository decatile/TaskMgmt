from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import mapped_column, relationship, Mapped
from .user import User
from .base import Base


class EmailVerification(Base):
    __tablename__ = "email_verification"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[int] = mapped_column(Integer())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship()

    def __repr__(self) -> str:
        return f"EmailVerification(id={self.id!r}, code={self.code!r}, user_id={self.user_id!r}, {self.ts_repr()})"
