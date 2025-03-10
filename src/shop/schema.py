from typing import List

from pydantic import BaseModel


class SProduct(BaseModel):
    id: int
    name: str
    price: float
    count: int
    description: str


class SCartProduct(BaseModel):
    product_id: int
    quantity: int


class SCart(BaseModel):
    id: int
    quantity: int
    user_id: int
    cart_products: List[SCartProduct]


class SProductAdd(BaseModel):
    product_id: int
    quantity: int = 1


class SProductRemove(BaseModel):
    product_id: int
    quantity: int = 1