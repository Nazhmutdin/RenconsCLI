import typing
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