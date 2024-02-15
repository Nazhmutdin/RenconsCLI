from sqlalchemy import BinaryExpression, select, and_, or_, desc

from src.models import WelderCertificationModel
from src.utils.db_objects import (
    WelderCertificationDataBaseRequest
)
from src.utils.base_repository import BaseRepository
from src.utils.UoW import SQLalchemyUnitOfWork
from src.shemas import (
    WelderCertificationShema
)


class WelderCertificationRepository(BaseRepository[WelderCertificationShema, WelderCertificationModel]):
    __tablemodel__ = WelderCertificationModel
    __shema__ = WelderCertificationShema

    def get_many(self, request: WelderCertificationDataBaseRequest | None = None) -> list[WelderCertificationShema]:
        with SQLalchemyUnitOfWork() as transaction:

            stmt = select(WelderCertificationModel).order_by(desc(WelderCertificationModel.certification_date))

            if request != None:
                or_expressions, and_expressions = self._get_expressions(request)

                stmt.filter(
                    or_(*or_expressions),
                    and_(*and_expressions)
                ).distinct()

            return [WelderCertificationShema.model_validate(el) for el in transaction.connection.execute(stmt).mappings().all()]


    def _get_expressions(self, request: WelderCertificationDataBaseRequest) -> tuple[list[BinaryExpression], list[BinaryExpression]]:
        or_expressions: list[BinaryExpression] = []
        and_expressions: list[BinaryExpression] = []

        if request.ids:
            or_expressions.append(WelderCertificationModel.certification_id.in_(request.ids))

        if request.kleymos:
            or_expressions.append(WelderCertificationModel.kleymo.in_(request.kleymos))
        
        if request.certification_numbers:
            or_expressions.append(WelderCertificationModel.certification_number.in_(request.certification_numbers))

        if request.certification_date_before:
            and_expressions.append(WelderCertificationModel.certification_date <= request.certification_date_before)

        if request.certification_date_from:
            and_expressions.append(WelderCertificationModel.certification_date >= request.certification_date_from)

        if request.expiration_date_before:
            and_expressions.append(WelderCertificationModel.expiration_date <= request.expiration_date_before)

        if request.expiration_date_from:
            and_expressions.append(WelderCertificationModel.expiration_date >= request.expiration_date_from)

        if request.expiration_date_fact_before:
            and_expressions.append(WelderCertificationModel.expiration_date_fact <= request.expiration_date_fact_before)
            
        if request.expiration_date_fact_from:
            and_expressions.append(WelderCertificationModel.expiration_date_fact >= request.expiration_date_fact_from)

        return (or_expressions, and_expressions)