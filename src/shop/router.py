from fastapi import APIRouter, HTTPException, status, Response, Depends



router = APIRouter(
    prefix="/shop",
    tags=["Магазин"]
)

@router.get("/get/", summary="Все товары")
async def get_all_product():
    return "всё"

@router.get("/get/{item_id}", summary="Информация о конкретном товаре")
async def get_item_by_id(item_id: int):
    return {"item_id": item_id}


@router.get("/cart/", summary="Информация о конкретной корзине пользователя")
async def get_user_cart():
    return "Информация о корзине"
@router.post("/cart/product/{item_id}", summary="Добавить товар в корзину")
async def add_product_to_cart(item_id: int):
    return {"item_id": item_id}