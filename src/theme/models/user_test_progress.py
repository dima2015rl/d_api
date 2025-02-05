
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class UserTestProgress(Base):
    __tablename__ = "user_test_progress"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user1.id"), nullable=False)
    test_id: Mapped[int] = mapped_column(ForeignKey("tests.id"), nullable=False)
    attempts_left: Mapped[int] = mapped_column(Integer, default=3, nullable=False)  # Осталось попыток
    best_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # Лучший результат
    last_attempt: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # Время последней попытки

    # Связи
    user: Mapped["User"] = relationship("User", back_populates="test_progress")
    test: Mapped["Test"] = relationship("Test")
