from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, relationship, Mapped
from ..user import User
from ..base_model import Base


class EmailVerification(Base):
    __tablename__ = "email_verification"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(4))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship()

    def __repr__(self) -> str:
        return f"EmailVerification(id={self.id!r}, code={self.code!r}, user_id={self.user_id!r}, {self.timestamps})"
