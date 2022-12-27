import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth, users
from app.database.init_db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
env = os.environ.get("ENV", "dev")

if env != "dev":
    app = FastAPI(docs_url=None, redoc_url=None)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(users.router)
