from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped

from database import Base


class Cart(Base):
    __tablename__ = "cart"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user1.id"), nullable=False)

    user = relationship("User", back_populates="cart")
    cart_products = relationship("CartProduct", back_populates="cart")