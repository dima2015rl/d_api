from fastapi import APIRouter, HTTPException, status, Response, Depends

from auth import get_password_hash, create_access_token, authericate_user
from src.auth.schema import SUserRegister, SUserAuth, SUserView
from src.auth.user_dao import UserDAO
from src.auth.dependecies import get_current_user
from src.auth.models import User

router = APIRouter(
    prefix="/users",
    tags=["Работа с пользователями"]
)


@router.get("/get_all/", summary="Получить всех пользователей")
async def get_all_users():
    return await UserDAO.find_all()


@router.post("/register/", summary="Зарегать пользователя")
async def register_user(user_data: SUserRegister):
    existing_user = await UserDAO.find_one_or_none(login=user_data.login)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists.")
    user_data_dict = user_data.model_dump(exclude_unset=True)
    user_data_dict["password_hash"] = get_password_hash(user_data_dict.pop("password"))
    await UserDAO.add(user_data_dict)
    return {"message": "Зарегали чела"}


@router.post("/login/", summary="Логин пользователя")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authericate_user(user_data.login, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    acess_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", acess_token, httponly=True)
    return response.status_code


@router.post("/logout/", summary="Пользователь выходит :<")
async def logout_user(responce:Response):
    responce.delete_cookie("access_token")
    return {"message": "Пользователь выходит :<"}


@router.get("/me/", summary="информация о пользователе")
async def read_users_me(current_user: User = Depends(get_current_user)):
    user_data = current_user.__dict__  # Получаем атрибуты модели SQLAlchemy
    user_data['password'] = current_user.password_hash  # Преобразуем password_hash в password
    del user_data['password_hash']  # Убираем password_hash из данных
    # Возвращаем данные через Pydantic модель
    return SUserRegister(**user_data)
