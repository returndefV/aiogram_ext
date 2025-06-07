from aiogram_ext.notification.strategies.info_strategy import InfoStrategy
from aiogram_ext.notification.context import NotificationContext


class DialogStrategy(InfoStrategy):

    async def send_notification(self, context: NotificationContext):
        await self.message.delete()
        try:
            await self.bot.delete_message(
                chat_id=self.chat_id,
                message_id=context.bot_last_msg_id
            )
        except Exception:
            pass

        await super().send_notification(context)
