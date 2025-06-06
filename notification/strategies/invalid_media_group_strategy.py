from aiogram_ext.notification.context import NotificationContext
from aiogram_ext.notification.strategies.base import NotificationStrategy


class InvalidMediaGroupStrategy(NotificationStrategy):

    async def send_notification(self, context: NotificationContext):
        for msg_id in context.media_group_msg_ids:
            try:
                await self.bot.delete_message(chat_id=self.chat_id, message_id=msg_id)
            except Exception:
                pass
