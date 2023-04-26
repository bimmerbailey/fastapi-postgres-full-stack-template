from fastapi import APIRouter, Depends, status, HTTPException, Cookie, Request
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from app import models, utils, oauth, crud
from app.database.init_db import get_db
from app.schemas import users
from app.config.config import settings

router = APIRouter(tags=["Authentication"], prefix="/api/v1")


@router.post("/login", response_model=users.Token)
async def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await crud.users.user.get_by_email(
        db=db, email=user_credentials.username
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Credentials",
        )

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Credentials",
        )

    access_token = oauth.create_access_token(
        data={"user_id": user.id, "is_admin": user.is_admin}
    )

    response = JSONResponse(
        content={
            "access_token": access_token,
            "token_type": "bearer",
            "is_admin": user.is_admin,
        }
    )
    response.set_cookie(
        key="token",
        value=access_token,
        expires=settings.access_token_expire_minutes * 60,
        domain=settings.url_base,
        httponly=False,
        secure=True,
    )
    return response


@router.get("/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="token", domain=settings.url_base)
    return response


@router.get("/authenticated", response_model=users.UserBase)
def read_user_me(
    db: AsyncSession = Depends(get_db),
    current_user: models.users.Users = Depends(oauth.get_current_user),
):
    return current_user.__dict__


@router.get("/forgot/password", response_model=users.UserBase)
def forgot_password(req: Request, db: AsyncSession = Depends(get_db)):
    body = req.query_params
    email = body.get("email", None)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Must give email"
        )

    forgotten_user = crud.users.user.get_by_email(db=db, email=email)
    if not forgotten_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"User not found"
        )

    return forgotten_user.__dict__
