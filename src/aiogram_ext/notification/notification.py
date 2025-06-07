from typing import Dict, List, Optional

from aiogram import Bot, Dispatcher
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from aiogram_ext.enums.notification_type import NotificationType
from aiogram_ext.notification.context import NotificationContext

from sqlalchemy.ext.asyncio import AsyncSession


class Notification:
    """A class for managing notifications in aiogram bots."""

    def __init__(
        self,
        *,
        bot: Bot,
        dispatcher: Dispatcher,
        sqlite_session: AsyncSession,
        message: Optional[Message] = None,
        callback: Optional[CallbackQuery] = None,
    ):
        self.bot = bot
        self.dispatcher = dispatcher
        self.sqlite_session = sqlite_session
        self.message = message
        self.callback = callback

        if message is None and callback is None:
            raise RuntimeError("Either 'message' or 'callback' must be provided in data")


    async def send(
        self,
        notification_type: NotificationType,
        *,
        msg: Optional[str] = None,
        media: Optional[Dict[str, str]] = None,
        media_caption: Optional[str] = None,
        kbd: Optional[InlineKeyboardMarkup] = None,
        button_text: Optional[List[List[str]]] = None,
        callback_data: Optional[List[List[str]]] = None,
        sizes: tuple[int] = (1,),
        media_group_msg_ids: Optional[List[int]] = None,
        menu_msg_id: Optional[int] = None,
        bot_last_msg_id: Optional[List[int]] = None,
        delay_time: int = 1
    ):
        """
        Use this method to send a notification.

        **NOTE**: The method is used only in private chats.

        **NOTE**: Cannot use both 'kbd' and 'button_text'/'callback_data' parameters together.

        :param notification_type: Notification type (:class:`aiogram_ext.enums.notification_type.NotificationType`)
        :param msg: A string to form a message (4096 characters)
        :param media: Dictionary, where the key is the media type, the value is file_id
        :param media_caption: A string used to form a description of the media
        :param kbd: Ready keyboard object
        :param button_text: List of lists, for forming a message on buttons
        :param callback_data: List of lists to form `callback_data` buttons
        :param sizes: The tuple used to form the keyboard, determines how many buttons will be in one line
        :param media_group_msg_ids: List of message_id media group objects
        :param menu_msg_id: Menu ID
        :param bot_last_msg_id: ID of the bot's last message(s)
        :param delay_time: The amount of time after which the message will be deleted. Applicable if the notification type `auto_delay` is selected. Defaults to 1 second
        """

        if kbd is not None and (button_text is not None or callback_data is not None):
            raise ValueError("Cannot use both 'kbd' and 'button_text'/'callback_data' parameters together")


        context = NotificationContext(
            msg=msg,
            media=media,
            media_caption=media_caption,
            kbd=kbd,
            button_text=button_text,
            callback_data=callback_data,
            sizes=sizes,
            media_group_msg_ids=media_group_msg_ids,
            menu_msg_id=menu_msg_id,
            bot_last_msg_id=bot_last_msg_id,
            delay_time=delay_time
        )

        from aiogram_ext.notification.factory import get_strategy
        strategy = get_strategy(notification_type, self)

        await strategy.send_notification(context)
