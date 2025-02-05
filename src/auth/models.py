from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from database import Base


class User(Base):
    __tablename__ = "user1"
    id: Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    login: Mapped[str] = mapped_column(String, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[str] = mapped_column(String,nullable=False)

