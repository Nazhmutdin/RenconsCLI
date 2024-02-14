from sqlalchemy import Select, select, desc
from sqlalchemy.orm import subqueryload

from src.models import WelderNDTModel, WelderModel
from src.utils.db_objects import (
    WelderNDTDataBaseRequest
)
from src.utils.base_repository import BaseRepository
from src.utils.UoW import SQLalchemyUnitOfWork
from src.shemas import WelderNDTShema


class WelderNDTRepository(BaseRepository[WelderNDTShema, WelderNDTModel]):
    __tablemodel__ = WelderNDTModel
    __shema__ = WelderNDTShema

    def get_many(self, request: WelderNDTDataBaseRequest | None = None) -> list[WelderNDTShema]:
        with SQLalchemyUnitOfWork() as transaction:

            stmt = select(WelderNDTModel).order_by(desc(WelderNDTModel.welding_date))

            if request == None:
                return [WelderNDTShema.model_validate(el) for el in transaction.connection.execute(stmt).mappings().all()]

            stmt = self._set_filters(stmt, request)
            return [WelderNDTShema.model_validate(el) for el in transaction.connection.execute(stmt).mappings().all()]



    def _set_filters(self, stmt: Select, request: WelderNDTDataBaseRequest) -> Select:

        if request.limit:
            stmt = stmt.limit(request.limit)

        if request.offset:
            stmt = stmt.offset(request.offset)

        if request.kleymos:
            stmt = stmt.filter(WelderNDTModel.kleymo.in_(request.kleymos))

        if request.comps:
            stmt = stmt.filter(WelderNDTModel.comp.in_(request.comps))

        if request.subcomps:
            stmt = stmt.filter(WelderNDTModel.subcon.in_(request.subcomps))

        if request.projects:
            stmt = stmt.filter(WelderNDTModel.project.in_(request.projects))

        if request.welding_date_before:
            stmt = stmt.filter(WelderNDTModel.welding_date <= request.welding_date_before)

        if request.welding_date_from:
            stmt = stmt.filter(WelderNDTModel.welding_date >= request.welding_date_from)

        if request.names:
            stmt = stmt.filter(WelderModel.name.in_(request.names))

        return stmt
