import logging

from aiogram import F, Dispatcher
from aiogram.fsm.context import FSMContext

from aiogram_ext.enums.notification_type import NotificationType
from aiogram_ext.notification.notification import Notification
from aiogram_ext.storage.sqlite_storage.models import TableNotificationMessage

logger = logging.getLogger(__name__)


def register_notification_handlers(dispatcher: Dispatcher) -> None:
    """Register global handlers for notifications."""

    dispatcher.callback_query.register(
        _delete_notification_handler,
        F.data.startswith("delete_notification")
    )
    logger.debug('Registered `delete_notification` handler for dispatcher %s', dispatcher)

    dispatcher.callback_query.register(
        _clear_state,
        F.data == "clear_fsm_state"
    )
    logger.debug('Registered `clear_fsm_state` handler for dispatcher %s', dispatcher)


async def _clear_state(notification: Notification, state: FSMContext):
    """Clear FSMContext"""

    await notification.send(NotificationType.CLOSE_NOTIFICATION)
    await state.clear()
    await notification.callback.answer("State clear")


async def _delete_notification_handler(notification: Notification):
    """Delete the notification."""

    key = notification.callback.data.split("_")[-1]
    record = await TableNotificationMessage.get_notification_by_key(key, notification.sqlite_session)

    try:
        await notification.bot.delete_message(chat_id=record.chat_id, message_id=record.msg_id)
    except Exception:
        pass

    await TableNotificationMessage.close_last_notification_by_key(key, notification.sqlite_session)

    await notification.callback.answer("Notification removed")
