from src.shop.dao.cart_dao import CartDAO
from src.shop.models.cart import Cart
from src.shop.models.cart_product import CartProduct
from sqlalchemy import select, delete
from database import async_session
from src.dao.base import BaseDAO

class CartProductDAO(BaseDAO):
    model = CartProduct

    @classmethod
    async def add_product_to_cart(cls, user_id: int, product_id: int, quantity: int = 1):
        """Добавить товар в корзину (если есть – увеличить количество)."""
        async with async_session() as session:
            cart = await CartDAO.get_user_cart(user_id)

            query = select(CartProduct).filter_by(cart_id=cart.id, product_id=product_id)
            result = await session.execute(query)
            cart_product = result.scalar_one_or_none()

            if cart_product:
                cart_product.quantity += quantity
            else:
                cart_product = CartProduct(cart_id=cart.id, product_id=product_id, quantity=quantity)
                session.add(cart_product)

            await session.commit()
            await session.refresh(cart_product)
            return cart_product

    @classmethod
    async def remove_product_from_cart(cls, user_id: int, product_id: int, quantity: int = 1):
        """Удалить товар из корзины (уменьшить количество или удалить полностью)."""
        async with async_session() as session:
            cart = await CartDAO.get_user_cart(user_id)

            query = select(CartProduct).filter_by(cart_id=cart.id, product_id=product_id)
            result = await session.execute(query)
            cart_product = result.scalar_one_or_none()

            if cart_product:
                if cart_product.quantity > quantity:
                    cart_product.quantity -= quantity
                else:
                    await session.execute(delete(CartProduct).where(CartProduct.id == cart_product.id))

                await session.commit()

    @classmethod
    async def get_cart_products(cls, user_id: int):
        """Получить все товары в корзине пользователя."""
        async with async_session() as session:
            cart = await CartDAO.get_user_cart(user_id)
            query = select(CartProduct).filter_by(cart_id=cart.id)
            result = await session.execute(query)
            return result.scalars().all()
