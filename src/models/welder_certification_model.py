from sqlalchemy import String, Column, Date, ForeignKey, Float, ARRAY

from src.db_engine import Base



class WelderCertificationModel(Base):
    __tablename__ = "welder_certification_table"

    kleymo = Column(String(4), ForeignKey("welder_table.kleymo"))
    certification_id = Column(String(), primary_key=True)
    job_title = Column(String(), nullable=True)
    certification_number = Column(String())
    certification_date = Column(Date())
    expiration_date = Column(Date())
    expiration_date_fact = Column(Date())
    insert = Column(String(), nullable=True)
    certification_type = Column(String(), nullable=True)
    company = Column(String(), nullable=True)
    gtd = Column(ARRAY(String), nullable=True)
    method = Column(String(), nullable=True)
    details_type = Column(ARRAY(String), nullable=True)
    joint_type = Column(ARRAY(String), nullable=True)
    groups_materials_for_welding = Column(ARRAY(String), nullable=True)
    welding_materials = Column(String(), nullable=True)
    details_thikness_from = Column(Float(), nullable=True)
    details_thikness_before = Column(Float(), nullable=True)
    outer_diameter_from = Column(Float(), nullable=True)
    outer_diameter_before = Column(Float(), nullable=True)
    welding_position = Column(String(), nullable=True)
    connection_type = Column(String(), nullable=True)
    rod_diameter_from = Column(Float(), nullable=True)
    rod_diameter_before = Column(Float(), nullable=True)
    rod_axis_position = Column(String(), nullable=True)
    weld_type = Column(String(), nullable=True)
    joint_layer = Column(String(), nullable=True)
    sdr = Column(String(), nullable=True)
    automation_level = Column(String(), nullable=True)
    details_diameter_from = Column(Float(), nullable=True)
    details_diameter_before = Column(Float(), nullable=True)
    welding_equipment = Column(String(), nullable=True)
