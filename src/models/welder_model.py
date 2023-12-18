from sqlalchemy import String, Column, Date, SMALLINT
from sqlalchemy.orm import Mapped, relationship

from src.db_engine import Base
from src.models.welder_certification_model import WelderCertificationModel
from src.models.welder_ndt_model import WelderNDTModel


class WelderModel(Base):
    __tablename__ = "welder_table"

    kleymo = Column(String(4), primary_key=True)
    name = Column(String(), nullable=True)
    birthday = Column(Date(), nullable=True)
    sicil_number = Column(String(), nullable=True)
    passport_id = Column(String(), nullable=True)
    sicil_number = Column(String(), nullable=True)
    nation = Column(String(), nullable=True)
    status = Column(SMALLINT)
    certifications = relationship("WelderCertificationModel", backref="welder")
    ndts = relationship("WelderNDTModel", backref="welder")
