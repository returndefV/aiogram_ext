from aiogram_ext.notification.context import NotificationContext
from aiogram_ext.notification.strategies.base import NotificationStrategy
from aiogram_ext.storage.sqlite_storage.models import TableMenuMessage


class CloseMenuStrategy(NotificationStrategy):

    async def send_notification(self, context: NotificationContext):
        records = await TableMenuMessage.get_last_menus(self.chat_id, self.sqlite_session)

        try:
            await self.bot.delete_messages(chat_id=self.chat_id, message_ids=records)
        except Exception:
            pass

        try:
            await TableMenuMessage.close_last_menus(self.chat_id, records, self.sqlite_session)
        except Exception:
            pass
