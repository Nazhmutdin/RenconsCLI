from datetime import date
from re import fullmatch

from pydantic import Field, field_validator

from src.models import WelderModel
from src.utils.base_shema import BaseShema
from src.shemas.welder_certification_shema import WelderCertificationShema


class WelderShema(BaseShema):
    __table_model__ = WelderModel
    kleymo: str = Field()
    name: str | None  = Field(default=None)
    birthday: date | None  = Field(default=None)
    passport_id: str | None = Field(default=None)
    sicil_number: str | None = Field(default=None)
    nation: str | None = Field(default=None)
    status: int = Field(default=0)
    certifications: list[WelderCertificationShema] = Field(default=[])


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
