from src.utils.base_repository import BaseRepository
from src.shemas import UserShema
from src.models import UserModel


class UserRepository(BaseRepository[UserShema, UserModel]):
    __tablemodel__ = UserModel
    __shema__ = UserShema
