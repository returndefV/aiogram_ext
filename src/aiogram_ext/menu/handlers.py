import logging

from aiogram import Router
from aiogram.types import InputMediaPhoto
from aiogram.filters import Command

from aiogram_ext.enums.notification_type import NotificationType
from aiogram_ext.notification.notification import Notification
from aiogram_ext.menu.callback import MenuCallBack
from aiogram_ext.menu.registry import MenuRegistry

logger = logging.getLogger(__name__)

menu = Router()


@menu.message(Command("menu"))
async def menu_command_handler(notification: Notification):
    try:
        await notification.send(NotificationType.CLOSE_MENU)

        content, keyboard = await MenuRegistry.create(
            sqlite_session=notification.sqlite_session,
            bot=notification.bot,
            name="main"
        )

        if isinstance(content, InputMediaPhoto):
            await notification.send(
                NotificationType.START_MENU,
                media=content,
                media_caption=content.caption,
                kbd=keyboard
            )

        elif isinstance(content, str):
            await notification.send(
                NotificationType.START_MENU,
                kbd=keyboard
            )

        else:
            raise ValueError("Unsupported content type")

    except Exception as e:
        logger.error("Error calling menu_command_handler: %s", e, exc_info=True)


@menu.callback_query(MenuCallBack.filter())
async def menu_callback_handler(notification: Notification, callback_data: MenuCallBack):
    try:
        content, keyboard = await MenuRegistry.create(
            sqlite_session=notification.sqlite_session,
            bot=notification.bot,
            name=callback_data.name,
        )

        if isinstance(content, InputMediaPhoto):
            await notification.send(
                NotificationType.EDIT_MENU,
                media=content,
                kbd=keyboard
            )

        elif isinstance(content, str):
            await notification.send(
                NotificationType.EDIT_MENU,
                kbd=keyboard
            )

        else:
            raise ValueError("Unsupported content type")

        await notification.callback.answer()

    except Exception as e:
        print(e)
        await notification.callback.answer("An error occurred")
