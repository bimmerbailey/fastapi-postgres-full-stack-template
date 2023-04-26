from typing import List

from fastapi import status, Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.schemas.users import UserOut, UserCreate
from app.crud.users import user
from app.models.users import Users
from app import oauth
from app.database.init_db import get_db

router = APIRouter(prefix="/api/v1/users", tags=["Users"])
logger: structlog.stdlib.BoundLogger = structlog.getLogger(__name__)


@router.get("", response_model=List[UserOut])
async def get_users(
    # current_user: Users = Depends(oauth.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    users = await user.get_all(db=db)
    return users


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(
    new_user: UserCreate, db: AsyncSession = Depends(get_db)
):
    db_user = await user.get_by_email(email=new_user.email, db=db)
    if db_user is not None:
        raise HTTPException(status_code=400, detail="Email already registered")
    some = await user.create(db=db, obj_in=new_user)
    return some.__dict__


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    db_user = await user.get_one(db=db, model_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    return db_user.__dict__
