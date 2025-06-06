from typing import Dict

from aiogram.types import InputMediaPhoto, InputMediaVideo

from aiogram_ext.keyboard.keyboard import Keyboard
from aiogram_ext.media.media import NotificationMedia
from aiogram_ext.notification.context import NotificationContext
from aiogram_ext.notification.strategies.base import NotificationStrategy
from aiogram_ext.storage.sqlite_storage.models import TableNotificationMessage


class MediaStrategy(NotificationStrategy):

    async def send_notification(self, context: NotificationContext):
        key = Keyboard.generate_key(self.chat_id)

        if context.kbd is not None:
            keyboard = context.kbd

        elif context.button_text is not None and context.callback_data is not None:
            keyboard = Keyboard.constructor_callback_btns(
                button_text=context.button_text,
                callback_data=context.callback_data,
                key=key,
                sizes=context.sizes
            )

        else:
            keyboard = None

        media_dict: Dict[str, str] = context.media
        media_type, media_id = next(iter(media_dict.items()))

        media = NotificationMedia.create_input_media(media_type, media_id)

        if isinstance(media, InputMediaPhoto):
            msg = await self.bot.send_photo(
                chat_id=self.chat_id,
                photo=media.media,
                caption=context.media_caption,
                reply_markup=keyboard
            )

        elif isinstance(media, InputMediaVideo):
            msg = await self.bot.send_video(
                chat_id=self.chat_id,
                video=media.media,
                caption=context.media_caption,
                reply_markup=keyboard
            )

        else:
            raise ValueError("Unsupported InputMedia type")

        await TableNotificationMessage.save_notification_message_id(self.chat_id, [msg.message_id], key, self.sqlite_session)
