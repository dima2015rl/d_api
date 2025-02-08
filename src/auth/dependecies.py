from datetime import datetime, timedelta

import jwt
from fastapi import Request, HTTPException, Depends
from jose import jws, JWTError

import config
from src.auth.user_dao import UserDAO


def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401)
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=[config.algoritm])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")

    expire: int = payload.get("exp")
    if not expire or datetime.utcnow().timestamp() > expire:
        raise HTTPException(status_code=402, detail="Token is invalid or expired.")

    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=403, detail="User ID not found in token.")

    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user

