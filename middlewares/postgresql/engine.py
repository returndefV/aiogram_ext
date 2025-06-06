from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from aiogram_ext.middlewares.postgresql.config import postgresql_config

from aiogram_ext.middlewares.postgresql.exceptions import PostgresqlDatabaseCreationError, PostgresqlDatabaseDropError

from database.models import Base # Specify the path to the file containing the abstract table "Base".


postgresql_engine = create_async_engine(postgresql_config.DATABASE_URL, poolclass=NullPool)

postgresql_session_maker = async_sessionmaker(bind=postgresql_engine, class_=AsyncSession, expire_on_commit=False)


class PostgresqlDatabase:

    async def create_postgresql_db(self):
        try:
            async with postgresql_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

        except Exception as e:
            raise PostgresqlDatabaseCreationError(f"An error occurred while creating tables: {e}") from e

    async def drop_postgresql_db(self):
        try:
            async with postgresql_engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)

        except Exception as e:
            raise PostgresqlDatabaseDropError(f"An error occurred while resetting the database: {e}") from e

postgresql = PostgresqlDatabase()
