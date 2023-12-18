from datetime import date
from re import fullmatch, findall

from pydantic import ConfigDict, Field, field_validator

from src.models import WelderCertificationModel
from src.utils.base_shema import BaseShema


class WelderCertificationShema(BaseShema):
    __table_model__ = WelderCertificationModel
    kleymo: str = Field()
    certification_id: str = Field()
    job_title: str | None = Field(default=None)
    certification_number: str = Field()
    certification_date: date = Field()
    expiration_date: date = Field()
    expiration_date_fact: date = Field()
    insert: str | None = Field(default=None)
    certification_type: str | None = Field(default=None)
    company: str | None = Field(default=None)
    gtd: list[str] | None = Field(default=None)
    method: str | None = Field(default=None)
    details_type: list[str] | None = Field(default=None)
    joint_type: list[str] | None = Field(default=None)
    groups_materials_for_welding: list[str] | None = Field(default=None)
    welding_materials: str | None = Field(default=None)
    details_thikness_from: float | None = Field(default=None)
    details_thikness_before: float | None = Field(default=None)
    outer_diameter_from: float | None = Field(default=None)
    outer_diameter_before: float | None = Field(default=None)
    welding_position: str | None = Field(default=None)
    connection_type: str | None = Field(default=None)
    rod_diameter_from: float | None = Field(default=None)
    rod_diameter_before: float | None = Field(default=None)
    rod_axis_position: str | None = Field(default=None)
    weld_type: str | None = Field(default=None)
    joint_layer: str | None = Field(default=None)
    sdr: str | None = Field(default=None)
    automation_level: str | None = Field(default=None)
    details_diameter_from: float | None = Field(default=None)
    details_diameter_before: float | None = Field(default=None)
    welding_equipment: str | None = Field(default=None)


    model_config = ConfigDict(
        populate_by_name=True,
    )


    @staticmethod
    def compute_certification_id(kleymo: str | int, certification_number: str, certification_date: date, insert: str) -> str:
        return f"{str(kleymo)}{"".join(findall(r"[\w]", certification_number))}{"".join(findall(r"[\w]", certification_date.strftime("%Y-%m-%d")))}{insert}".lower()


    @field_validator("kleymo")
    def validate_kleymo(cls, v: str) -> str:
        
        if fullmatch(r"[A-Z0-9]{4}", v.strip()):
            return v.strip()
        
        raise ValueError(f"Invalid kleymo ===> {v}")
