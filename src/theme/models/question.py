from typing import List

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base


class Question(Base):
    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    points: Mapped[int] = mapped_column(Integer, nullable=False)

    true_answer: Mapped["QuestionTrueAnswer"] = relationship("QuestionTrueAnswer", back_populates="question",
                                                             uselist=False)
    wrong_answers: Mapped[List["WrongAnswer"]] = relationship("WrongAnswer", back_populates="question")




