from src.utils.base_repository import BaseRepository
from src.shemas import UserShema
from src.models import UserModel
from src.utils.db_objects import DBResponse, DataBaseRequest


class UserRepository(BaseRepository):
    __tablemodel__ = UserModel
    __shema__ = UserShema
