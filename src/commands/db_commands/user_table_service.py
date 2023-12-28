from typing import TypedDict, Unpack
from datetime import datetime

from src.utils.funcs import hash_password
from src.repositories import UserRepository
from src.shemas import UserShema


class UserDict(TypedDict):
    name: str
    login: str
    password: str
    email: str | None
    is_superuser: bool


repo = UserRepository()


def add_user(**kwargs: Unpack[UserDict]) -> None:
    kwargs["hashed_password"] = hash_password(kwargs["password"])
    user = UserShema.model_validate(kwargs, from_attributes=True)

    user.set_sign_date()
    user.set_login_date()
    user.set_update_date()
    repo.add(user)


def update_user(login: str, **kwargs: Unpack[UserDict]) -> None:
    kwargs = {key: value for key, value in kwargs.items() if value != None}

    kwargs["update_date"] = datetime.utcnow()
    repo.update(login, **kwargs)
