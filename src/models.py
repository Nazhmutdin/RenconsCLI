from datetime import datetime, date

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import String, Column, Date, ForeignKey, Float, ARRAY, Boolean, DateTime, SMALLINT

from src.db_engine import Base


class UserModel(Base):
    __tablename__ = "user_table"
    name: Mapped[str] = Column(String())
    login: Mapped[str] = Column(String(), primary_key=True)
    hashed_password: Mapped[str] = Column(String())
    email: Mapped[str | None] = Column(String(), nullable=True)
    sign_date: Mapped[datetime] = Column(DateTime())
    update_date: Mapped[datetime] = Column(DateTime())
    login_date: Mapped[datetime] = Column(DateTime())
    is_superuser: Mapped[bool] = Column(Boolean())


class WelderModel(Base):
    __tablename__ = "welder_table"

    kleymo: Mapped[str] = Column(String(4), primary_key=True)
    name: Mapped[str] = Column(String(), nullable=True)
    birthday: Mapped[str | None] = Column(Date(), nullable=True)
    sicil_number: Mapped[str | None] = Column(String(), nullable=True)
    passport_id: Mapped[str | None] = Column(String(), nullable=True)
    sicil_number: Mapped[str | None] = Column(String(), nullable=True)
    nation: Mapped[str | None] = Column(String(), nullable=True)
    status: Mapped[str] = Column(SMALLINT)
    certifications: Mapped[list["WelderCertificationModel"]] = relationship("WelderCertificationModel", back_populates="welder")
    ndts: Mapped[list["WelderNDTModel"]] = relationship("WelderNDTModel", back_populates="welder")


class WelderCertificationModel(Base):
    __tablename__ = "welder_certification_table"

    kleymo: Mapped[str] = Column(String(4), ForeignKey("welder_table.kleymo"))
    certification_id: Mapped[str] = Column(String(), primary_key=True)
    job_title: Mapped[str] = Column(String(), nullable=True)
    certification_number: Mapped[str] = Column(String())
    certification_date: Mapped[date] = Column(Date())
    expiration_date: Mapped[date] = Column(Date())
    expiration_date_fact: Mapped[date] = Column(Date())
    insert: Mapped[str | None] = Column(String(), nullable=True)
    certification_type: Mapped[str | None] = Column(String(), nullable=True)
    company: Mapped[str | None] = Column(String(), nullable=True)
    gtd: Mapped[list[str]] | None = Column(ARRAY(String), nullable=True)
    method: Mapped[str] = Column(String(), nullable=True)
    details_type: Mapped[list[str] | None] = Column(ARRAY(String), nullable=True)
    joint_type: Mapped[list[str] | None] = Column(ARRAY(String), nullable=True)
    groups_materials_for_welding: Mapped[list[str] | None] = Column(ARRAY(String), nullable=True)
    welding_materials: Mapped[str | None] = Column(String(), nullable=True)
    details_thikness_from: Mapped[float | None] = Column(Float(), nullable=True)
    details_thikness_before: Mapped[float | None] = Column(Float(), nullable=True)
    outer_diameter_from: Mapped[float | None] = Column(Float(), nullable=True)
    outer_diameter_before: Mapped[float | None] = Column(Float(), nullable=True)
    welding_position: Mapped[str | None] = Column(String(), nullable=True)
    connection_type: Mapped[str | None] = Column(String(), nullable=True)
    rod_diameter_from: Mapped[float | None] = Column(Float(), nullable=True)
    rod_diameter_before: Mapped[float | None] = Column(Float(), nullable=True)
    rod_axis_position: Mapped[str | None] = Column(String(), nullable=True)
    weld_type: Mapped[str | None] = Column(String(), nullable=True)
    joint_layer: Mapped[str | None] = Column(String(), nullable=True)
    sdr: Mapped[str | None] = Column(String(), nullable=True)
    automation_level: Mapped[str | None] = Column(String(), nullable=True)
    details_diameter_from: Mapped[float | None] = Column(Float(), nullable=True)
    details_diameter_before: Mapped[float | None] = Column(Float(), nullable=True)
    welding_equipment: Mapped[str | None] = Column(String(), nullable=True)

    welder: Mapped[WelderModel] = relationship("WelderModel", back_populates="certifications")


class WelderNDTModel(Base):
    __tablename__ = "welder_ndt_table"
    
    kleymo: Mapped[str] = Column(String(4), ForeignKey("welder_table.kleymo"))
    comp: Mapped[str | None] = Column(String(), nullable=True)
    subcon: Mapped[str | None] = Column(String(), nullable=True)
    project: Mapped[str | None] = Column(String(), nullable=True)
    welding_date: Mapped[date] = Column(Date())
    total_weld_1: Mapped[float | None] = Column(Float(), nullable=True)
    total_ndt_1: Mapped[float | None] = Column(Float(), nullable=True)
    total_accepted_1: Mapped[float | None] = Column(Float(), nullable=True)
    total_repair_1: Mapped[float | None] = Column(Float(), nullable=True)
    repair_status_1: Mapped[float | None] = Column(Float(), nullable=True)
    total_weld_2: Mapped[float | None] = Column(Float(), nullable=True)
    total_ndt_2: Mapped[float | None] = Column(Float(), nullable=True)
    total_accepted_2: Mapped[float | None] = Column(Float(), nullable=True)
    total_repair_2: Mapped[float | None] = Column(Float(), nullable=True)
    repair_status_2: Mapped[float | None] = Column(Float(), nullable=True)
    total_weld_3: Mapped[float | None] = Column(Float(), nullable=True)
    total_ndt_3: Mapped[float | None] = Column(Float(), nullable=True)
    total_accepted_3: Mapped[float | None] = Column(Float(), nullable=True)
    total_repair_3: Mapped[float | None] = Column(Float(), nullable=True)
    repair_status_3: Mapped[float | None] = Column(Float(), nullable=True)
    ndt_id: Mapped[str] = Column(String(), primary_key=True)
    
    welder: Mapped[WelderModel] = relationship("WelderModel", back_populates="ndts")
