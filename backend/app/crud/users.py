from typing import Any, Optional, Union

from sqlalchemy.orm import Session

from app.utils import hash_password, verify
from app.crud.base import CrudBase
from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate


class CRUDUser(CrudBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(self.model).filter(User.email == email).first()

    def get_users(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()

    @classmethod
    def create(cls, db: Session, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            password=hash_password(obj_in.password),
            is_admin=obj_in.is_admin
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = hash_password(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user_auth = self.get_by_email(db, email=email)
        if not user_auth:
            return None
        if not verify(password, user_auth.hashed_password):
            return None
        return user_auth

    @property
    def is_active(self) -> bool:
        return user.is_active

    @property
    def is_admin(self) -> bool:
        return user.is_admin


user = CRUDUser(User)
