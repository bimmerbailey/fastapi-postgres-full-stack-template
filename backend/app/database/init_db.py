from typing import AsyncIterator

import structlog
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config.config import settings

logger = structlog.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.database_username}:{settings.database_password}@"
    f"{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    future=True,
)


# Dependency
async def get_db() -> AsyncIterator[async_sessionmaker]:
    try:
        async with AsyncSessionLocal() as session:
            yield session
    except SQLAlchemyError as e:
        logger.exception(e)
        await session.rollback()
        raise
    finally:
        await session.close()


async def close_db_connection():
    logger.info("Closing connection to database...")
    await engine.dispose()
    logger.info("Connection closed!")
