from src.dao.base import BaseDAO
from src.shop.models.product import Product


class ProductDAO(BaseDAO):
    model = Product