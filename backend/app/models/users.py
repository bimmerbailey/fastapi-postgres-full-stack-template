from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP
from sqlalchemy.sql.expression import text

from .base import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    created_date = Column(
        TIMESTAMP(timezone=True), server_default=text("now()")
    )
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, server_default="false")
