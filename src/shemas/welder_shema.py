from datetime import date
from typing import Union
from re import fullmatch
from pydantic import Field, field_validator

from src.models import WelderModel
from src.utils.base_shema import BaseShema
from src.shemas.welder_certification_shema import WelderCertificationShema
from src.shemas.welder_ndt_shema import WelderNDTShema


class WelderShema(BaseShema):
    __table_model__ = WelderModel
    kleymo: str = Field()
    name: Union[str, None] = Field(default=None)
    birthday: Union[date, None] = Field(default=None)
    passport_id: Union[str, None] = Field(default=None)
    sicil_number: Union[str, None] = Field(default=None)
    nation: Union[str, None] = Field(default=None)
    status: int = Field(default=0)
    certifications: list[WelderCertificationShema] = Field(default=[])
    ndts: list[WelderNDTShema] = Field(default=[])


    @field_validator("kleymo")
    def validate_kleymo(cls, v: str):
        if fullmatch(r"[A-Z0-9]{4}", v.strip()):
            return v
        
        raise ValueError(f"Invalid kleymo: {v}")


    def __eq__(self, __value: "WelderShema") -> bool:
        if not super().__eq__(__value):
            return False
        
        if len(__value.certifications) != len(self.certifications):
            return False
        
        for i in range(len(self.certifications)):
            if self.certifications[i] != __value.certifications[i]:
                return False
            
        return True
