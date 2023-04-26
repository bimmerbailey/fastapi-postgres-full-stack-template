from typing import Any, Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import ScalarResult

from app.utils import hash_password, verify
from app.crud.base import CrudBase
from app.models.users import Users
from app.schemas.users import UserCreate, UserUpdate


class CRUDUser(CrudBase[Users, UserCreate, UserUpdate]):
    async def get_by_email(
        self, db: AsyncSession, email: str
    ) -> Optional[Users]:
        stmt = select(self.model).where(self.model.email == email)
        return (await db.execute(stmt)).scalar_one_or_none()

    async def create(self, db: AsyncSession, obj_in: UserCreate) -> Users:
        db_obj = Users(
            email=obj_in.email,
            password=hash_password(obj_in.password),
            is_admin=obj_in.is_admin,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: Users,
        obj_in: Union[UserUpdate, dict[str, Any]]
    ) -> Users:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = hash_password(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def authenticate(
        self, db: AsyncSession, *, email: str, password: str
    ) -> Optional[Users]:
        user = await self.get_by_email(db=db, email=email)
        if not user:
            return None
        if not verify(password, user.password):
            return None
        return user

    @property
    def is_admin(self) -> bool:
        return self.model.is_admin


user = CRUDUser(Users)
