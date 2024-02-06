from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from sqlmodel import SQLModel, Session, select
from asyncpg.exceptions import PostgresError
from logging import getLogger

# logger
logger = getLogger("vibraphile")

ModelType = TypeVar("ModelType", bound=Any)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD)

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        try:
            id_name: str = self.model.__table__.primary_key.columns.keys()[0]
            return db.execute(select(self.model).filter(
                getattr(self.model, id_name) == id),
                execution_options={"prebuffer_rows": True}).first()
        except PostgresError as e:
            logger.exception("An error occurred from the database\n",
                             exc_info=e)
            raise
        except Exception as e:
            logger.exception("An error occurred\n", exc_info=e)
            raise

    def get_all(self, db: Session) -> Optional[ModelType]:
        try:
            id_name: str = self.model.__table__.primary_key.columns.keys()[0]
            return db.execute(select(getattr(self.model, id_name)),
                              execution_options={"prebuffer_rows": True})
        except PostgresError as e:
            logger.exception("An error occurred from the database\n",
                             exc_info=e)
            raise
        except Exception as e:
            logger.exception("An error occurred\n", exc_info=e)
            raise

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
