from typing import Generic, Type, TypeVar, Any, Optional, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc, select, Sequence
from sqlalchemy.engine import Row

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CrudBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with async default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A Beanie Document class
        """
        self.model = model

    async def get_all(
        self, db: AsyncSession, skip: int = 0, limit: int = 20
    ) -> Sequence:
        print(self.model)
        return [
            i.__dict__
            for i in (
                await db.execute(
                    select(self.model)
                    .limit(limit)
                    .offset(skip)
                    .order_by(desc("created_date"))
                )
            )
            .scalars()
            .all()
        ]

    async def get_one(self, db: AsyncSession, model_id: Any) -> Row:
        stmt = select(self.model).where(self.model.id == int(model_id))
        return (await db.execute(stmt)).scalar_one_or_none()

    async def create(
        self, db: AsyncSession, obj_in: CreateSchemaType
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, dict[str, Any]],
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
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, model_id: int) -> ModelType:
        obj = db.query(self.model).get(model_id)
        await db.delete(obj)
        await db.commit()
        return obj

    async def filter(
        self, db: AsyncSession, column: ModelType, value: str
    ) -> list:
        stmt = select(self.model).where(self.model[column] == value)
        return (await db.execute(stmt)).scalar_one_or_none()
