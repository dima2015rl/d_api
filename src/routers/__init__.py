from fastapi import APIRouter
from src.auth.router import router as auth_router
from src.theme.router import router as theme_router
main_router = APIRouter() #главный роутер

# Подключение маршрутов
main_router.include_router(auth_router)
main_router.include_router(theme_router)