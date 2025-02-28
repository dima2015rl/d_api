from src.shop.models.cart import Cart
from sqlalchemy import select
from database import async_session
from src.dao.base import BaseDAO

class CartDAO(BaseDAO):
    model = Cart

    @classmethod
    async def get_user_cart(cls, user_id: int):
        """Получить корзину пользователя (или создать, если её нет) """
        async with async_session() as session:
            query = select(Cart).filter_by(user_id=user_id)
            result = await session.execute(query)
            cart = result.scalar_one_or_none()

            if not cart:
                cart = Cart(user_id=user_id)
                session.add(cart)
                await session.commit()
                await session.refresh(cart)

            return cart