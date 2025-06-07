from abc import ABC, abstractmethod
from typing import Optional

from aiogram import Bot
from aiogram.types import Message, CallbackQuery

from aiogram_ext.notification.context import NotificationContext
from aiogram_ext.notification.notification import Notification

from sqlalchemy.ext.asyncio import AsyncSession


class NotificationStrategy(ABC):
    def __init__(self, notification: Notification):
        self.notification = notification

    @property
    def bot(self) -> Bot:
        return self.notification.bot

    @property
    def sqlite_session(self) -> AsyncSession:
        return self.notification.sqlite_session

    @property
    def message(self) -> Optional[Message]:
        return self.notification.message

    @property
    def callback(self) -> Optional[CallbackQuery]:
        return self.notification.callback

    @property
    def chat_id(self) -> int:
        if self.message:
            return self.message.chat.id
        elif self.callback:
            return self.callback.message.chat.id
        raise ValueError("No message or callback available")

    @abstractmethod
    async def send_notification(self, context: NotificationContext):
        pass
