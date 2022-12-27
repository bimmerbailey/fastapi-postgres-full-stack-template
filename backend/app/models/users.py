from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP
from sqlalchemy.sql.expression import text

from app.database.init_db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    created_date = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, server_default="false")
