import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname = os.environ.get("DATABASE_HOST", "postgres")
    database_port = os.environ.get("DATABASE_PORT", "5432")
    database_password = os.environ.get("DATABASE_PASSWORD", "Password123!")
    database_name = os.environ.get("DATABASE_NAME", "your_app")
    database_username = os.environ.get("DATABASE_USERNAME", "postgres")
    secret_key = os.environ.get("JWT_SECRET_KEY", "secret")
    algorithm = os.environ.get("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes = os.environ.get("JWT_TOKEN_EXPIRES", 60)
    url_base = os.environ.get("URL_BASE", "localhost")


settings = Settings()
