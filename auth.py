from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from starlette import status

import config
from src.auth.user_dao import UserDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash_password: str) -> bool:
    return pwd_context.verify(password, hash_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode
                            , config.secret_key,
                            config.algoritm)
    return encode_jwt


async def authericate_user(login: str, password: str):
    user = await UserDAO.find_one_or_none(login=login)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user
