from typing import Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy import Select, Connection, update, insert, delete, inspect, select, func
from sqlalchemy.sql.schema import Column

from src.db_engine import BaseModel
from src.utils.db_objects import (
    DataBaseRequest
)

from src.utils.base_shema import BaseShema
from src.utils.UoW import SQLalchemyUnitOfWork


class BaseRepository[Shema: BaseShema, Model: BaseModel]:
    __tablemodel__: Model
    __shema__: Shema


    def get(self, id: str | int) -> Shema | None:
        with SQLalchemyUnitOfWork() as transaction:
            stmt = select(self.__tablemodel__).where(
                self.pk == id
            )

            res = transaction.session.execute(stmt).fetchone()

            result = self.__shema__.model_validate(
                res[0], 
                from_attributes=True
            ) if res != None else None

        if result != None:
            return result


    def get_many(self, request: DataBaseRequest) -> list[Shema]: ...


    def add(self, model: Shema) -> None:
        with SQLalchemyUnitOfWork() as transaction:
            try:
                stmt = insert(self.__tablemodel__).values(**model.orm_data)

                transaction.connection.execute(stmt)

                transaction.commit()

            except IntegrityError as e:
                    
                transaction.rollback()


    def update(self, id: Any, **kwargs) -> None:
        with SQLalchemyUnitOfWork() as transaction:
            try:
                stmt = update(self.__tablemodel__).where(
                    self.pk == id
                ).values(**kwargs)

                transaction.connection.execute(stmt)

                transaction.commit()

            except IntegrityError as e:
                print(e)
                transaction.rollback()


    def delete(self, id: Any) -> None:
        with SQLalchemyUnitOfWork() as transaction:
            try:
                stmt = delete(self.__tablemodel__).where(
                    self.pk == id
                )
                
                transaction.connection.execute(stmt)

                transaction.commit()

            except IntegrityError as e:
                print(e)
                transaction.rollback()


    def count(self, stmt: Select | None = None, connection: Connection | None = None) -> int:
        if connection and stmt != None:

            count = len(connection.execute(stmt).all())

        elif connection and stmt == None:
            count = connection.execute(select(func.count()).select_from(self.__tablemodel__)).scalar()

        else:
            with SQLalchemyUnitOfWork() as transaction:

                count = transaction.connection.execute(select(func.count()).select_from(self.__tablemodel__)).scalar()

        return count


    @property
    def pk(self) -> Column:
        return inspect(self.__tablemodel__).primary_key[0]
