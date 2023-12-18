from sqlalchemy import String, Column, Date, ForeignKey, Float
from sqlalchemy.orm import Mapped, relationship

from src.db_engine import Base


class WelderNDTModel(Base):
    __tablename__ = "welder_ndt_table"
    
    kleymo = Column(String(4), ForeignKey("welder_table.kleymo"))
    comp = Column(String(), nullable=True)
    subcon = Column(String(), nullable=True)
    project = Column(String(), nullable=True)
    welding_date = Column(Date(), nullable=True)
    total_weld_1 = Column(Float(), nullable=True)
    total_ndt_1 = Column(Float(), nullable=True)
    total_accepted_1 = Column(Float(), nullable=True)
    total_repair_1 = Column(Float(), nullable=True)
    repair_status_1 = Column(Float(), nullable=True)
    total_weld_2 = Column(Float(), nullable=True)
    total_ndt_2 = Column(Float(), nullable=True)
    total_accepted_2 = Column(Float(), nullable=True)
    total_repair_2 = Column(Float(), nullable=True)
    repair_status_2 = Column(Float(), nullable=True)
    total_weld_3 = Column(Float(), nullable=True)
    total_ndt_3 = Column(Float(), nullable=True)
    total_accepted_3 = Column(Float(), nullable=True)
    total_repair_3 = Column(Float(), nullable=True)
    repair_status_3 = Column(Float(), nullable=True)
    ndt_id = Column(String(), primary_key=True)
