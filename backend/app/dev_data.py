from sqlalchemy.orm import Session

from app.models.users import User
from app.database.init_db import SessionLocal
from app.utils import hash_password


def create_users(session: Session) -> None:
    admin_user = User(
        email="admin@your_app.com",
        password=hash_password("password"),
        is_admin=True
    )
    session.add(admin_user)
    session.commit()
    session.refresh(admin_user)
    reg_user = User(
        email="user@your_app.com",
        password=hash_password("password"),
    )
    session.add(reg_user)
    session.commit()
    session.refresh(reg_user)


def local_data(session: Session) -> None:
    for table in [User]:
        session.query(table).delete()
        session.commit()
    create_users(session)


def get_local_data() -> None:
    local_data(SessionLocal())


if __name__ == '__main__':
    get_local_data()
