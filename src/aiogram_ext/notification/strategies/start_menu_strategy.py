from aiogram.types import InputMediaPhoto

from aiogram_ext.notification.context import NotificationContext
from aiogram_ext.notification.strategies.base import NotificationStrategy
from aiogram_ext.storage.sqlite_storage.models import TableMenuMessage


class StartMenuStrategy(NotificationStrategy):

    async def send_notification(self, context: NotificationContext):
        try:
            await self.message.delete()
        except Exception:
            pass

        if isinstance(context.media, InputMediaPhoto):
            menu = await self.bot.send_photo(
                chat_id=self.chat_id,
                photo=context.media.media,
                caption=context.msg,
                reply_markup=context.kbd
            )

        elif context.media is None:
            menu = await self.bot.send_message(
                chat_id=self.chat_id,
                text=context.msg,
                reply_markup=context.kbd
            )

        else:
            raise ValueError("Unsupported menu type")

        await TableMenuMessage.save_menu_message_id(self.chat_id, [menu.message_id], self.sqlite_session)
