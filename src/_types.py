import typing as t
from datetime import date


class WelderData(t.TypedDict):
    kleymo: str
    name: str
    birthday: date
    passport_id: str
    sicil_number: str
    nation: str
    status: int


class WelderCertificationData(t.TypedDict):
    kleymo: str
    certification_id: str
    job_title: str
    certification_number: str
    certification_date: date
    expiration_date: date
    expiration_date_fact: date
    insert: str | None
    certification_type: str | None
    company: str | None
    gtd: list[str] | None
    method: str
    details_type: list[str] | None
    joint_type: list[str] | None
    groups_materials_for_welding: list[str] | None
    welding_materials: str | None
    details_thikness_from: float | None
    details_thikness_before: float | None
    outer_diameter_from: float | None
    outer_diameter_before: float | None
    welding_position: str | None
    connection_type: str | None
    rod_diameter_from: float | None
    rod_diameter_before: float | None
    rod_axis_position: str | None
    weld_type: str | None
    joint_layer: str | None
    sdr: str | None
    automation_level: str | None
    details_diameter_from: float | None
    details_diameter_before: float | None
    welding_equipment: str | None



class WelderNDTData(t.TypedDict):
    kleymo: str
    comp: str | None
    subcon: str | None
    project: str | None
    welding_date: date
    total_weld_1: float | None
    total_ndt_1: float | None
    total_accepted_1: float | None
    total_repair_1: float | None
    repair_status_1: float | None
    total_weld_2: float | None
    total_ndt_2: float | None
    total_accepted_2: float | None
    total_repair_2: float | None
    repair_status_2: float | None
    total_weld_3: float | None
    total_ndt_3: float | None
    total_accepted_3: float | None
    total_repair_3: float | None
    repair_status_3: float | None
    ndt_id: str


class UserData(t.TypedDict):
    name: str
    login: str
    password: str
    email: str | None
    is_active: bool
    is_superuser: bool