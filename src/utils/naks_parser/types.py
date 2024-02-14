from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class NaksFilters(BaseModel): ...


class PersonalNaksFilters(NaksFilters):
    search_values: Optional[list[str]] = Field(default=None)
    certification_date_from: Optional[date] = Field(default=None)
    certification_date_before: Optional[date] = Field(default=None)
    expiration_date_from: Optional[date] = Field(default=None)
    expiration_date_before: Optional[date] = Field(default=None)
    renewal_date_from: Optional[date] = Field(default=None)
    renewal_date_before: Optional[date] = Field(default=None)
    methods: Optional[list[str]] = Field(default=None)
    gtd: Optional[list[str]] = Field(default=None)


class WelderData(BaseModel):
    name: str | None = Field(default=None)
    kleymo: str | None = Field(default=None)
    job_title: str | None = Field(default=None)
    company: str | None = Field(default=None, alias="Место работы (организация, инн):")
    certification_date: date | None = Field(default=None)
    expiration_date: date | None = Field(default=None)
    expiration_date_fact: date | None = Field(default=None)
    certification_number: str | None = Field(default=None)
    certification_type: str | None = Field(default=None, alias="Вид аттестации:")
    insert: str | None = Field(default=None)
    method: str | None = Field(default=None, alias="Вид (способ) сварки (наплавки)")
    details_type: list[str] = Field(default=[])
    joint_type: list[str] = Field(default=[])
    groups_materials_for_welding: list[str] = Field(default=[])
    welding_materials: str | None = Field(default=None, alias="Сварочные материалы")
    details_thikness_from: float | None = Field(default=None)
    details_thikness_before: float | None = Field(default=None)
    outer_diameter_from: float | None = Field(default=None)
    outer_diameter_before: float | None = Field(default=None)
    welding_position: str | None = Field(default=None, alias="Положение при сварке")
    connection_type: str | None = Field(default=None, alias="Вид соединения")
    rod_diameter_from: float | None = Field(default=None)
    rod_diameter_before: float | None = Field(default=None)
    rod_axis_position: str | None = Field(default=None, alias="Положение осей стержней")
    weld_type: str | None = Field(default=None, alias="Тип сварного соединения")
    joint_layer: str | None = Field(default=None, alias="Слой шва")
    gtd: list[str] = Field(default=[])
    sdr: str | None = Field(default=None, alias="SDR")
    automation_level: str | None = Field( default=None, alias="Степень автоматизации")
    details_diameter_from: float | None = Field(default=None)
    details_diameter_before: float | None = Field(default=None)
    welding_equipment: str | None = Field(default=None, alias="Сварочное оборудование")
    certification_id: str = Field()

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
