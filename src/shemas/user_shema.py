from datetime import datetime

from pydantic import Field

from src.utils.base_shema import BaseShema
from src.models import UserModel


class UserShema(BaseShema):
    __table_model__ = UserModel
    name: str = Field()
    login: str = Field()
    hashed_password: str = Field()
    email: str | None = Field(default=None)
    sign_date: datetime = Field(default_factory=datetime.utcnow)
    update_date: datetime = Field(default_factory=datetime.utcnow)
    login_date: datetime = Field(default_factory=datetime.utcnow)
    is_superuser: bool = Field(default=False)
