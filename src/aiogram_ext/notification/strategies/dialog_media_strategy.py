from aiogram_ext.notification.context import NotificationContext
from aiogram_ext.notification.strategies.media_strategy import MediaStrategy


class DialogMediaStrategy(MediaStrategy):

    async def send_notification(self, context: NotificationContext):
        await self.message.delete()
        await super().send_notification(context)
