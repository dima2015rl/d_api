from typing import List

from pydantic import BaseModel

class SProduct(BaseModel):
    id: int
    name: str
    price: float
    count: int
    description: str




class SProductAdd(BaseModel):
    product_id: int
    quantity: int = 1

class SProductRemove(BaseModel):
    product_id: int
    quantity: int = 1