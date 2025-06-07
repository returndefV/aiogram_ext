from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from aiogram_ext.logger.telegram_logger import TelegramLogger


class TelegramLoggerMiddleware(BaseMiddleware):
    """Middleware for dependency injection TelegramLogger in handlers."""

    def __init__(self, telegram_logger: TelegramLogger):
        super().__init__()
        self.telegram_logger = telegram_logger

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        data['telegram_logger'] = self.telegram_logger
        return await handler(event, data)
