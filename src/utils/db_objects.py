from datetime import date

from pydantic import BaseModel, Field

from src.utils.base_shema import BaseShema


class DataBaseRequest(BaseModel):
    limit: int = Field(default=100)
    offset: int = Field(default=0)


class WelderCertificationDataBaseRequest(DataBaseRequest):
    kleymos: list[str] = Field(default=[])
    ids: list[str] = Field(default=[])
    certification_numbers: list[str] = Field(default=[])
    certification_date_from: date | None = Field(default=None)
    certification_date_before: date | None = Field(default=None)
    expiration_date_from: date | None = Field(default=None)
    expiration_date_before: date | None = Field(default=None)
    expiration_date_fact_from: date | None = Field(default=None)
    expiration_date_fact_before: date | None = Field(default=None)
    details_thikness_from: float | None = Field(default=None)
    details_thikness_before: float | None = Field(default=None)
    outer_diameter_from: float | None = Field(default=None)
    outer_diameter_before: float | None = Field(default=None)
    rod_diameter_from: float | None = Field(default=None)
    rod_diameter_before: float | None = Field(default=None)
    details_diameter_from: float | None = Field(default=None)
    details_diameter_before: float | None = Field(default=None)
    gtd: list[str] = Field(default=[])
    method: list[str] = Field(default=[])


class WelderDataBaseRequest(WelderCertificationDataBaseRequest):
    names: list[str] | None = Field(default=None)


class WelderNDTDataBaseRequest(DataBaseRequest):
    names: list[str] | None = Field(default=None)
    kleymos: list[str | int] | None = Field(default=None)
    comps: list[str] | None = Field(default=None)
    subcomps: list[str] | None = Field(default=None)
    projects: list[str] | None = Field(default=None)
    welding_date_from: date | None = Field(default=None)
    welding_date_before: date | None = Field(default=None)


class DBResponse[Model:BaseShema](BaseModel):
    count: int
    result: list[Model]