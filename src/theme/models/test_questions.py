from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class TestQuestion(Base):
    __tablename__ = "test_questions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    test_id: Mapped[int] = mapped_column(ForeignKey("tests.id"), nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False)

    test: Mapped["Test"] = relationship("Test", back_populates="questions")
    question: Mapped["Question"] = relationship("Question")
