from pydantic import BaseModel

class SProductAdd(BaseModel):
    id: int
    quantity:int