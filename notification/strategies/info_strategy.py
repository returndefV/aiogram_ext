from aiogram_ext.keyboard.keyboard import Keyboard
from aiogram_ext.notification.context import NotificationContext
from aiogram_ext.notification.strategies.base import NotificationStrategy
from aiogram_ext.storage.sqlite_storage.models import TableNotificationMessage


class InfoStrategy(NotificationStrategy):

    async def send_notification(self, context: NotificationContext):
        if context.kbd is not None:
            keyboard = context.kbd

        else:
            key = Keyboard.generate_key(self.chat_id)
            keyboard = Keyboard.constructor_callback_btns(
                button_text=context.button_text,
                callback_data=context.callback_data,
                key=key,
                sizes=context.sizes
            )

        msg = await self.bot.send_message(
            chat_id=self.chat_id,
            text=context.msg,
            reply_markup=keyboard
        )

        await TableNotificationMessage.save_notification_message_id(self.chat_id, [msg.message_id], key, self.sqlite_session)
