from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base


class Theme(Base):
    __tablename__ = "themes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    tests: Mapped[list["Test"]] = relationship("Test", back_populates="theme")


