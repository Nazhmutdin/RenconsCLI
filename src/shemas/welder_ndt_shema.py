from datetime import date
from re import fullmatch, sub

from pydantic import Field, field_validator

from src.models import WelderNDTModel
from src.utils.base_shema import BaseShema


class WelderNDTShema(BaseShema):
    __table_model__ = WelderNDTModel
    kleymo: str | int = Field(default=None)
    comp: str | None = Field(default=None)
    subcon: str | None = Field(default=None)
    project: str | None = Field(default=None)
    welding_date: date = Field()
    total_weld_1: float | None = Field(default=None)
    total_ndt_1: float | None = Field(default=None)
    total_accepted_1: float | None = Field(default=None)
    total_repair_1: float | None = Field(default=None)
    repair_status_1: float | None = Field(default=None)
    total_weld_2: float | None = Field(default=None)
    total_ndt_2: float | None = Field(default=None)
    total_accepted_2: float | None = Field(default=None)
    total_repair_2: float | None = Field(default=None)
    repair_status_2: float | None = Field(default=None)
    total_weld_3: float | None = Field(default=None)
    total_ndt_3: float | None = Field(default=None)
    total_accepted_3: float | None = Field(default=None)
    total_repair_3: float | None = Field(default=None)
    repair_status_3: float | None = Field(default=None)
    ndt_id: str = Field()


    @staticmethod
    def compute_ndt_id(kleymo: str, comp: str, subcomp: str, project: str, welding_date: date) -> str:
        return sub(
            r"\W",
            "",
            string=f"{kleymo}{comp}{subcomp}{project}{welding_date.strftime("%Y-%m-%d")}".lower()
        )


    @field_validator("welding_date")
    def validate_latest_welding_date(cls, v):
        if type(v) != date or v == None:
            raise ValueError("welding_date must be date type")
        
        return v


    @field_validator("kleymo")
    def validate_kleymo(cls, v) -> str:
        if not fullmatch(r"[A-Z0-9]{4}", str(v).strip()) or v == None:
            raise ValueError(f"Invalid kleymo ===> {v}")
        
        return str(v).strip()
