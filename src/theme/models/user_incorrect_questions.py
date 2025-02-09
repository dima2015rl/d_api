from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class UserIncorrectQuestion(Base):
    __tablename__ = "user_incorrect_questions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user1.id"), nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False)

    # Связи c пользователем и с вопросами
    user: Mapped["User"] = relationship("User", back_populates="incorrect_questions")
    question: Mapped["Question"] = relationship("Question")
