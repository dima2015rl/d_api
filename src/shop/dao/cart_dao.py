from sqlalchemy.orm import joinedload
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
            query = select(Cart).filter_by(user_id=user_id).options(joinedload(Cart.cart_products))
            result = await session.execute(query)
            cart = result.scalar_one_or_none()

            if not cart:
                cart = await CartDAO.add(Cart(user_id=user_id))

            return {
                "id": cart.id,
                "user_id": cart.user_id,
                "cart_products": [
                    {
                        "id": cp.id,
                        "product_id": cp.product_id,
                        "quantity": cp.quantity,
                    }
                    for cp in cart.cart_products  # cart_products будет пустым, но это ок
                ],
            }
