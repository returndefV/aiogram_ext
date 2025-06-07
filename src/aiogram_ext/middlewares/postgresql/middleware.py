from typing import Any, Awaitable, Callable, Dict
import logging

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

logger = logging.getLogger(__name__)


class PostgresqlSessionMiddleware(BaseMiddleware):
    """Middleware for managing database sessions with transaction support.
    
    **NOTE**: If you need to execute multiple database queries in one handler, they will be executed within a single transaction.
    
    **NOTE**: There is no need to explicitly write `commit`, `rollback` and `close`, the context manager does this.
    """

    def __init__(self, session_pool: async_sessionmaker[AsyncSession]):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data["postgresql_session"] = session
            logger.debug("Postgresql session created for handler")

            try:
                async with session.begin():
                    logger.debug("Transaction started")
                    result = await handler(event, data)
                    logger.debug("Transaction completed successfully")
                    return result

            except Exception as e:
                logger.error(
                    "Transaction rolled back due to error: %s",
                    e,
                    exc_info=True
                )
                raise

            finally:
                logger.debug("Postgresql session closed")
