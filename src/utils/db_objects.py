from datetime import date
import typing as t

from pydantic import BaseModel, Field


class DataBaseRequest(BaseModel):
    limit: t.Optional[int] = Field(default=None)
    offset: t.Optional[int] = Field(default=None)


class WelderCertificationDataBaseRequest(DataBaseRequest):
    kleymos: t.Optional[list[str | int]] = Field(default=None)
    ids: t.Optional[list[str]] = Field(default=None)
    certification_numbers: list[str] = Field(default=None)
    certification_date_from: t.Optional[date] = Field(default=None)
    certification_date_before: t.Optional[date] = Field(default=None)
    expiration_date_from: t.Optional[date] = Field(default=None)
    expiration_date_before: t.Optional[date] = Field(default=None)
    expiration_date_fact_from: t.Optional[date] = Field(default=None)
    expiration_date_fact_before: t.Optional[date] = Field(default=None)
    details_thikness_from: t.Optional[float] = Field(default=None)
    details_thikness_before: t.Optional[float] = Field(default=None)
    outer_diameter_from: t.Optional[float] = Field(default=None)
    outer_diameter_before: t.Optional[float] = Field(default=None)
    rod_diameter_from: t.Optional[float] = Field(default=None)
    rod_diameter_before: t.Optional[float] = Field(default=None)
    details_diameter_from: t.Optional[float] = Field(default=None)
    details_diameter_before: t.Optional[float] = Field(default=None)
    gtd: t.Optional[list[str]] = Field(default=None)
    method: t.Optional[list[str]] = Field(default=None)


class WelderDataBaseRequest(WelderCertificationDataBaseRequest):
    names: t.Optional[list[str]] = Field(default=None)


class WelderNDTDataBaseRequest(DataBaseRequest):
    names: t.Optional[list[str]] = Field(default=None)
    kleymos: t.Optional[list[str | int]] = Field(default=None)
    comps: t.Optional[list[str]] = Field(default=None)
    subcomps: t.Optional[list[str]] = Field(default=None)
    projects: t.Optional[list[str]] = Field(default=None)
    welding_date_from: t.Optional[date] = Field(default=None)
    welding_date_before: t.Optional[date] = Field(default=None)
