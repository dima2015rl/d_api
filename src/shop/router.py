from fastapi import APIRouter, HTTPException, status, Response, Depends

from src.auth.dependecies import get_current_user
from src.auth.models import User
from src.shop.dao.cart_dao import CartDAO
from src.shop.dao.cart_product_dao import CartProductDAO
from src.shop.dao.product_dao import ProductDAO
from src.shop.schema import SProductAdd

router = APIRouter(
    prefix="/shop",
    tags=["Магазин"]
)

@router.get("/get/", summary="Все товары")
async def get_all_product():
    return await ProductDAO.find_all()

@router.get("/get/{item_id}", summary="Информация о конкретном товаре")
async def get_item_by_id(item_id: int):
    return await ProductDAO.find_by_id(item_id)


@router.get("/cart/", summary="Информация о конкретной корзине пользователя")
async def get_user_cart(current_user: User = Depends(get_current_user)):
    bucket = CartDAO.get_user_cart(current_user.id)
    return ""
@router.post("/cart/product/", summary="Добавить товар в корзину")
async def add_product_to_cart(request: SProductAdd,current_user: User = Depends(get_current_user)):
    await CartProductDAO.add_product_to_cart(current_user.id, request.product_id, request.quantity)
    return ""
