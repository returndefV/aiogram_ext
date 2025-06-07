import asyncio
import logging
from typing import Callable, Any, Awaitable, Dict, List, Union

from aiogram import BaseMiddleware
from aiogram.types import Message

from aiogram_ext.notification.notification import Notification

logger = logging.getLogger(__name__)


class MediaMiddleware(BaseMiddleware):
    """Middleware for processing message albums in Telegram."""

    def __init__(self, latency: Union[int, float] = 1):
        self.latency = latency
        self.album_data: Dict[str, List[Message]] = {}

    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: dict[str, Any]
    ) -> Any:
        if isinstance(event, Notification):
            message = event.message
        elif isinstance(event, Message):
            message = event
        else:
            return await handler(event, data)

        if not message.media_group_id:
            return await handler(event, data)

        try:
            self.album_data.setdefault(message.media_group_id, []).append(message)

        except Exception as e:
            logger.error("Error adding message to album: %s", e, exc_info=True)
            return await handler(event, data)

        if len(self.album_data[message.media_group_id]) == 1:
            logger.info("New album detected: %s. Waiting %.1f seconds...", message.media_group_id, self.latency)
            await asyncio.sleep(self.latency)

            album_messages = self.album_data.pop(message.media_group_id, [])
            if album_messages:
                try:
                    data["album"] = album_messages
                    return await handler(event, data)
                except Exception as e:
                    logger.error("Error processing album: %s", e, exc_info=True)
                    # We clear in case of an error.
                    if message.media_group_id in self.album_data:
                        del self.album_data[message.media_group_id]
