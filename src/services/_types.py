from datetime import date
import typing as t

from pydantic import BaseModel, Field

from src.shemas import WelderNDTShema, WelderShema


class WelderMethodsData(BaseModel):
    RD_method_certification: str | None = Field(default="-")
    RD_method_certification_date: date | str = Field(default="-")
    RAD_method_certification: str | None = Field(default="-")
    RAD_method_certification_date: date | str = Field(default="-")
    MP_method_certification: str | None = Field(default="-")
    MP_method_certification_date: date | str = Field(default="-")
    MPG_method_certification: str | None = Field(default="-")
    MPG_method_certification_date: date | str = Field(default="-")


class WelderNDTRegistryRow(BaseModel):
    name: str | None  = Field(default=None)
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
    RD_method_certification: str | None = Field(default="-")
    RD_method_certification_date: date | str = Field(default="-")
    RAD_method_certification: str | None = Field(default="-")
    RAD_method_certification_date: date | str = Field(default="-")
    MP_method_certification: str | None = Field(default="-")
    MP_method_certification_date: date | str = Field(default="-")
    MPG_method_certification: str | None = Field(default="-")
    MPG_method_certification_date: date | str = Field(default="-")


    def as_list(self) -> list[str | int | date | float | None]:
        return [value for value in self.model_dump().values()]