from aiogram_ext.notification.context import NotificationContext
from aiogram_ext.notification.strategies.base import NotificationStrategy
from aiogram_ext.storage.sqlite_storage.models import TableNotificationMessage


class CloseNotification(NotificationStrategy):

    async def send_notification(self, context: NotificationContext):
        record = await TableNotificationMessage.get_last_notifications(self.chat_id, self.sqlite_session)

        try:
            await self.bot.delete_messages(self.chat_id, message_ids=record)
        except Exception:
            pass

        try:
            await TableNotificationMessage.close_last_notifications(self.chat_id, record, self.sqlite_session)
        except Exception:
            pass
