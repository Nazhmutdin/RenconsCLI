import typing as t

from src.repositories import WelderRepository, WelderNDTRepository, WelderCertificationRepository, UserRepository
from src.shemas import WelderShema, WelderNDTShema, WelderCertificationShema, UserShema
from src.utils.base_repository import BaseRepository
from src.utils.base_shema import BaseShema
from src._types import WelderData, WelderCertificationData, WelderNDTData, UserData


__all__ = [
    "WelderDataBaseService",
    "WelderCertificationDataBaseService",
    "WelderNDTDataBaseService"
]


class BaseDataBaseService:
    repo: BaseRepository = NotImplementedError
    shema: BaseShema = NotImplementedError

    def add(self, **kwargs) -> None:
        self.repo.add(self.shema.model_validate(kwargs))


    def update(self, ident: str | int, **kwargs) -> None:
        self.repo.update(ident, **kwargs)


class WelderDataBaseService(BaseDataBaseService):
    repo = WelderRepository()
    shema = WelderShema

    def add(self, **kwargs: t.Unpack[WelderData]) -> None: 
        super().add(**kwargs)
    
    def update(self, ident: str | int, **kwargs: t.Unpack[WelderData]) -> None:
        super().update(ident, **kwargs)


class WelderCertificationDataBaseService(BaseDataBaseService):
    repo = WelderCertificationRepository()
    shema = WelderCertificationShema

    def add(self, **kwargs: t.Unpack[WelderCertificationData]) -> None: 
        super().add(**kwargs)
    
    def update(self, ident: str | int, **kwargs: t.Unpack[WelderCertificationData]) -> None:
        super().update(ident, **kwargs)


class WelderNDTDataBaseService(BaseDataBaseService):
    repo = WelderNDTRepository()
    shema = WelderNDTShema

    def add(self, **kwargs: t.Unpack[WelderNDTData]) -> None: 
        super().add(**kwargs)
    
    def update(self, ident: str | int, **kwargs: t.Unpack[WelderNDTData]) -> None:
        super().update(ident, **kwargs)


class UserDataBaseService(BaseDataBaseService):
    repo = UserRepository()
    shema = UserShema

    def add(self, **kwargs: t.Unpack[UserData]) -> None: 
        super().add(**kwargs)
    
    def update(self, ident: str | int, **kwargs: t.Unpack[UserData]) -> None:
        super().update(ident, **kwargs)
