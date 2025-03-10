from typing import List

from fastapi import APIRouter, HTTPException, status, Response, Depends

from src.auth.dependecies import get_current_user
from src.auth.models import User
from src.shop.dao.cart_dao import CartDAO
from src.shop.dao.cart_product_dao import CartProductDAO
from src.shop.dao.product_dao import ProductDAO
from src.shop.schema import SProductAdd, SProduct, SProductRemove, SCartProduct

router = APIRouter(
    prefix="/shop",
    tags=["Магазин"]
)

@router.get("/get/", response_model=List[SProduct], summary="Все товары")
async def get_all_product():
    return await ProductDAO.find_all()

@router.get("/get/{item_id}", response_model=SProduct, summary="Информация о конкретном товаре")
async def get_item_by_id(item_id: int):
    return await ProductDAO.find_by_id(item_id)
'''
@router.get("/cart/", response_model=SCart, summary="Информация о конкретной корзине пользователя")
async def get_user_cart(current_user: User = Depends(get_current_user)):
    cart = await CartDAO.get_user_cart(current_user.id)
    return cart'''

@router.get("/cart/products/", response_model=List[SCartProduct], summary="Получить товары в корзине")
async def get_cart_products(current_user: User = Depends(get_current_user)):
    return await CartProductDAO.get_cart_products(current_user.id)

@router.post("/cart/product/", summary="Добавить товар в корзину")
async def add_product_to_cart(request: SProductAdd, current_user: User = Depends(get_current_user)):
    await CartProductDAO.add_product_to_cart(current_user.id, request.product_id, request.quantity)
    return {"message": "Товар добавлен в корзину"}

@router.delete("/cart/product/", summary="Удалить товар из корзины")
async def remove_product_from_cart(request: SProductRemove, current_user: User = Depends(get_current_user)):
    await CartProductDAO.remove_product_from_cart(current_user.id, request.product_id, request.quantity)
    return {"message": "Товар удален из корзины"}
