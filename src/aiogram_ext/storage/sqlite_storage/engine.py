from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from ..exceptions import SqliteDatabaseCreationError, SqliteDatabaseDropError

from .config import DB_SQLITE

from .models import Base


sqlite_engine = create_async_engine(DB_SQLITE)

sqlite_session_maker = async_sessionmaker(bind=sqlite_engine, class_=AsyncSession, expire_on_commit=False)



class SqliteDatabase:

    async def create_sqlite_db(self):
        try:
            async with sqlite_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

        except Exception as e:
            raise SqliteDatabaseCreationError(f"An error occurred while creating tables: {e}") from e
    
    async def drop_sqlite_db(self):
        try:
            async with sqlite_engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)

        except Exception as e:
            raise SqliteDatabaseDropError(f"An error occurred while resetting the database: {e}") from e

sqlite = SqliteDatabase()
