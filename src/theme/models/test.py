from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base


class Test(Base):
    __tablename__ = "tests"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    theme_id: Mapped[int] = mapped_column(ForeignKey("themes.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    theme: Mapped["Theme"] = relationship("Theme", back_populates="tests")
    questions: Mapped[list["TestQuestion"]] = relationship("TestQuestion", back_populates="test")

    @hybrid_property
    def max_score(self) -> int:
        return sum(question.question.points for question in self.questions)