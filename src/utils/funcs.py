import typing as t
import inspect
from datetime import date
from pathlib import Path
from json import load
import types

from dateutil.parser import parser
from passlib.context import CryptContext
from click import Option, option


def options_from_class(cls):
    def decorator(f):
        for par in inspect.signature(cls).parameters.values():
            if par.name not in ["self"]:
                option(f"--{par.name}", type=par.annotation)(f)
            
        return f
    
    return decorator


def get_options_from_class[cls_dict: t.TypedDict](cls: cls_dict) -> list[Option]:
    params = []
    for name, annotations in cls.__annotations__.items():
        params.append(
            Option([f"--{name}"], type=annotations, required=False)
        )

    return params


def load_json(path: str | Path) -> t.Any:
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
