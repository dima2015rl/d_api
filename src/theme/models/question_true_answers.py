from sqlalchemy import Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class QuestionTrueAnswer(Base):
    __tablename__ = "question_true_answers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False)
    answer_id: Mapped[int] = mapped_column(ForeignKey("answers.id"), nullable=False)

    question: Mapped["Question"] = relationship("Question", back_populates="true_answer")
    answer: Mapped["Answer"] = relationship("Answer")