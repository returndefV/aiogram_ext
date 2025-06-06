import asyncio

from aiogram_ext.notification.context import NotificationContext
from aiogram_ext.notification.strategies.base import NotificationStrategy


class AutoDelayStrategy(NotificationStrategy):

    async def send_notification(self, context: NotificationContext):
        msg = await self.bot.send_message(chat_id=self.chat_id, text=context.msg)

        await asyncio.sleep(context.delay_time)

        try:
            await self.bot.delete_message(chat_id=self.chat_id, message_id=msg.message_id)
        except Exception:
            pass
