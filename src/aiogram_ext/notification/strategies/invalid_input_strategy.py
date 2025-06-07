from aiogram_ext.notification.context import NotificationContext
from aiogram_ext.notification.strategies.info_strategy import InfoStrategy


class InvalidInputStrategy(InfoStrategy):

    async def send_notification(self, context: NotificationContext):
        await self.message.delete()
        await super().send_notification(context)
