from aiogram.types import InputMediaPhoto

from aiogram_ext.notification.context import NotificationContext
from aiogram_ext.notification.strategies.base import NotificationStrategy
from aiogram_ext.storage.sqlite_storage.models import TableMenuMessage


class EditMenuStrategy(NotificationStrategy):

    async def send_notification(self, context: NotificationContext):
        all_msgs = await TableMenuMessage.get_last_menus(self.chat_id, self.sqlite_session)

        last_msg_id = all_msgs[-1]

        old_msgs = all_msgs[:-1]
        for msg_id in old_msgs:
            try:
                await self.bot.delete_message(chat_id=self.chat_id, message_id=msg_id)
            except Exception:
                pass

        await TableMenuMessage.close_last_menus(self.chat_id, old_msgs, self.sqlite_session)

        if isinstance(context.media, InputMediaPhoto):
            await self.bot.edit_message_media(
                chat_id=self.chat_id,
                message_id=last_msg_id,
                media=context.media,
                reply_markup=context.kbd
            )
        elif context.media is None:
            await self.bot.edit_message_text(
                chat_id=self.chat_id,
                message_id=last_msg_id,
                text=context.msg,
                reply_markup=context.kbd
            )
        else:
            raise ValueError("Unsupported menu type")
