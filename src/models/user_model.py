from datetime import datetime

from sqlalchemy.orm import Mapped
from sqlalchemy import Column, Boolean, DateTime, String

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
