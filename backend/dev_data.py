import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from app.models.users import Users
from app.database.init_db import AsyncSessionLocal
from app.utils import hash_password


async def create_users(session: AsyncSession) -> None:
    admin_user = Users(
        email="admin@your_app.com",
        password=hash_password("password"),
        first_name="dev",
        last_name="admin",
        is_admin=True,
    )
    session.add(admin_user)
    await session.commit()
    await session.refresh(admin_user)
    reg_user = Users(
        email="user@your_app.com",
        first_name="dev",
        last_name="user",
        password=hash_password("password"),
    )
    session.add(reg_user)
    await session.commit()
    await session.refresh(reg_user)


async def local_data(session: AsyncSession) -> None:
    for table in [Users]:
        await session.execute(delete(table))
        await session.commit()
    await create_users(session)
    await session.close()


async def get_local_data() -> None:
    await local_data(AsyncSessionLocal())


if __name__ == "__main__":
    asyncio.run(get_local_data())
