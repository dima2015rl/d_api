from pydantic import BaseModel


class SUserRegister(BaseModel):  # пользователь при регистрации отправляет всё ниже
    name: str
    surname: str
    login: str
    password: str
    date: str


class SUserAuth(BaseModel):  # пользователь при входе отправляет всё ниже
    login: str
    password: str


class SUserView(BaseModel): # посмотреть пользователя просто
    name: str
    surname: str
    login: str
    password: str
    date: str
    balance: int
