from sqlalchemy import Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base

class ThemeProgress(Base):
    __tablename__ = 'theme_progress'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user1.id'))
    theme_id: Mapped[int] = mapped_column(Integer, ForeignKey('themes.id'))
    is_passed: Mapped[bool] = mapped_column(Boolean,default=True)