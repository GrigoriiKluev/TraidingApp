import datetime
# Миграции создаются через alembic  (alembic init migrations)
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import MetaData,Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from database import Base,metadata


role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),

)

# user = Table(
#     "user",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("email", String, nullable=False),
#     Column("username", String, nullable=False),
#     Column("hashed_password", String, nullable=False),
#     Column("registered_at", TIMESTAMP, default=datetime.datetime.utcnow),
#     Column("role_id", Integer, ForeignKey(role.c.id)),
#     Column("is_active",Boolean, default=True, nullable=False),
#     Column("is_superuser",Boolean, default=False, nullable=False),
#     Column("is_verified",Boolean, default=False, nullable=False),
# )


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    #password = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    role_id = Column(Integer, ForeignKey(role.c.id))

    # email: Mapped[str] = mapped_column(
    #     String(length=320), unique=True, index=True, nullable=False
    # )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )