import typing
from passlib.context import CryptContext
from datetime import date
from dateutil.parser import parser

from pathlib import Path
from json import load


def load_json(path: str | Path) -> typing.Any:
    return load(open(path, "r", encoding="utf-8"))


def str_to_date(date_string: str, dayfirst: bool = True) -> date | None:
    try:
        return parser().parse(date_string, dayfirst=dayfirst).date()

    except:
        return None
    

crypt_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return crypt_ctx.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return crypt_ctx.verify(password, hashed_password)
