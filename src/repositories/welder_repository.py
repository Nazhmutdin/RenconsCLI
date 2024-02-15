from sqlalchemy import BinaryExpression, select, and_, or_

from src.models import WelderCertificationModel, WelderModel
from src.utils.db_objects import (
    WelderDataBaseRequest
)
from src.utils.UoW import SQLalchemyUnitOfWork
from src.utils.base_repository import BaseRepository
from src.shemas import WelderShema


class WelderRepository(BaseRepository[WelderShema, WelderModel]):
    __tablemodel__ = WelderModel
    __shema__ = WelderShema


    def get_many(self, request: WelderDataBaseRequest | None = None) -> list[WelderShema]:
            
        with SQLalchemyUnitOfWork() as transaction:

            stmt = select(WelderModel).join(
                WelderCertificationModel
            ).distinct()

            if request != None:
                or_expressions, and_expressions = self._get_many_filtrating(request)
                stmt = select(WelderModel).join(
                    WelderCertificationModel
                ).filter(
                    or_(*or_expressions),
                    and_(*and_expressions)
                ).distinct()
                
                if request.limit:
                    stmt = stmt.limit(request.limit)
                
                if request.offset:
                    stmt = stmt.offset(request.offset)

            return [WelderShema.model_validate(welder[0], from_attributes=True) for welder in transaction.session.execute(stmt).all()]


    def _get_many_filtrating(self, request: WelderDataBaseRequest) -> tuple[list[BinaryExpression], list[BinaryExpression]]:
        or_expressions: list[BinaryExpression] = []
        and_expressions: list[BinaryExpression] = []

        if request.names:
            or_expressions.append(WelderModel.name.in_(request.names))

        if request.kleymos:
            or_expressions.append(WelderModel.kleymo.in_(request.kleymos))

        if request.certification_numbers:
            or_expressions.append(WelderCertificationModel.certification_number.in_(request.certification_numbers))

        return (or_expressions, and_expressions)
