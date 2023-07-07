# СОЗДАНИЕ АУТЕНТИФИКАЦИИ ПОЛЬЗОВАТЕЛЕЙ С ПОМОЩЬЮ БИБЛИОТЕКИ fastapi_users
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from config import DB_USER,DB_PASS,DB_HOST,DB_PORT,DB_NAME
from sqlalchemy import MetaData

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Base(DeclarativeBase):
    pass


# class User(SQLAlchemyBaseUserTable[int], Base):
#     id = Column(Integer, primary_key=True)
#     email = Column(String, nullable=False)
#     username = Column(String, nullable=False)
#     #password = Column(String, nullable=False)
#     registered_at = Column(TIMESTAMP, default=datetime.datetime.utcnow),
#     role_id = Column(Integer, ForeignKey(role.c.id))
#
#     # email: Mapped[str] = mapped_column(
#     #     String(length=320), unique=True, index=True, nullable=False
#     # )
#     hashed_password: Mapped[str] = mapped_column(
#         String(length=1024), nullable=False
#     )
#     is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
#     is_superuser: Mapped[bool] = mapped_column(
#         Boolean, default=False, nullable=False
#     )
#     is_verified: Mapped[bool] = mapped_column(
#         Boolean, default=False, nullable=False
#     )


metadata = MetaData()

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


#async def create_db_and_tables():
    #async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


# async def get_user_db(session: AsyncSession = Depends(get_async_session)):
#     yield SQLAlchemyUserDatabase(session, User)