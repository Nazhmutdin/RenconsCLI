from pydantic import Field

from src.utils.base_shema import BaseShema


class ACSTShema(BaseShema):

    acst: str
    company: str
