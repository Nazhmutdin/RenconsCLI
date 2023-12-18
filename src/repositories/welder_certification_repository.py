from sqlalchemy import BinaryExpression, select, and_, or_

from src.models import WelderCertificationModel
from src.utils.db_objects import (
    DBResponse,
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

    def get_many(self, request: WelderCertificationDataBaseRequest) -> DBResponse[WelderCertificationShema]:
        with SQLalchemyUnitOfWork() as transaction:

            or_expressions, and_expressions = self._get_many_filtrating(request)

            stmt = select(WelderCertificationModel).filter(
                and_(
                    or_(*or_expressions),
                     *and_expressions
                )
            )

            if request.limit:
                stmt = stmt.limit(request.limit)

            if request.offset:
                stmt = stmt.offset(request.offset)

            res = transaction.connection.execute(stmt).mappings().all()
            result = [WelderCertificationShema.model_validate(certification) for certification in res]

        return result


    def _get_many_filtrating(self, request: WelderCertificationDataBaseRequest) -> tuple[list[BinaryExpression], list[BinaryExpression]]:
        or_expressions: list[BinaryExpression] = []
        and_expressions: list[BinaryExpression] = []

        if request.ids:
            and_expressions.append(WelderCertificationModel.certification_id.in_(request.ids))
        
        if request.certification_numbers:
            and_expressions.append(WelderCertificationModel.certification_number.in_(request.certification_numbers))

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