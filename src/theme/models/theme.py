from sqlalchemy import String, Integer
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base


class Theme(Base):
    __tablename__ = "themes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    tests: Mapped[list["Test"]] = relationship("Test", back_populates="theme")
    points_to_access: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    @hybrid_property
    def max_score(self) -> int:
        return sum(test.max_score for test in self.tests)




