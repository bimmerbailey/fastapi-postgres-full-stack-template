import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth, users
from app.database.init_db import engine
from app.models.base import Base
from app.config.config import settings
from app.config.logging import setup_logging, setup_fastapi

setup_logging(json_logs=False, log_level=settings.log_level)
app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

if os.getenv("FASTAPI_ENV", None) != "development":
    app = FastAPI(docs_url=None, redoc_url=None)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_fastapi(app)
app.include_router(auth.router)
app.include_router(users.router)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()
