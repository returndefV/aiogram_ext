import logging
from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from aiogram_ext.notification.notification import Notification

logger = logging.getLogger(__name__)


class NotificationMiddleware(BaseMiddleware):
    """Middleware for Notification implementation."""

    def __init__(self):
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[Union[Message, CallbackQuery], dict], Awaitable],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ):
        logger.debug("[DEBUG] NotificationMiddleware triggered for %s", type(event))

        bot = data.get("bot")
        dispatcher = data.get("dispatcher")
        sqlite_session = data.get("sqlite_session")

        if not bot or not dispatcher or not sqlite_session:
            raise ValueError("Required bot, dispatcher or sqlite_session not found in middleware data")

        if isinstance(event, CallbackQuery):
            notification = Notification(
                bot=bot,
                dispatcher=dispatcher,
                message=event.message,
                callback=event,
                sqlite_session=sqlite_session
            )
            return await handler(notification, data)

        elif isinstance(event, Message):
            notification = Notification(
                bot=bot,
                dispatcher=dispatcher,
                message=event,
                sqlite_session=sqlite_session
            )
            return await handler(notification, data)

        return await handler(event, data)
