from aiogram_ext.enums.notification_type import NotificationType
from aiogram_ext.notification.strategies.close_notification_strategy import CloseNotification
from aiogram_ext.notification.strategies.edit_menu_strategy import EditMenuStrategy
from aiogram_ext.notification.strategies.close_menu_strategy import CloseMenuStrategy
from aiogram_ext.notification.strategies.info_strategy import InfoStrategy
from aiogram_ext.notification.strategies.auto_delay_strategy import AutoDelayStrategy
from aiogram_ext.notification.strategies.dialog_strategy import DialogStrategy
from aiogram_ext.notification.strategies.invalid_input_strategy import InvalidInputStrategy
from aiogram_ext.notification.strategies.invalid_media_group_strategy import InvalidMediaGroupStrategy
from aiogram_ext.notification.strategies.media_strategy import MediaStrategy
from aiogram_ext.notification.strategies.start_menu_strategy import StartMenuStrategy


def get_strategy(notification_type: NotificationType, notification):
    strategy_map = {
        NotificationType.AUTO_DELAY: AutoDelayStrategy,
        NotificationType.INFO: InfoStrategy,
        NotificationType.INVALID_INPUT: InvalidInputStrategy,
        NotificationType.INVALID_MEDIA_GROUP: InvalidMediaGroupStrategy,
        NotificationType.START_MENU: StartMenuStrategy,
        NotificationType.EDIT_MENU: EditMenuStrategy,
        NotificationType.CLOSE_MENU: CloseMenuStrategy,
        NotificationType.CLOSE_NOTIFICATION: CloseNotification,
        NotificationType.DIALOG: DialogStrategy,
        NotificationType.MEDIA: MediaStrategy,
    }

    if strategy_class := strategy_map.get(notification_type):
        return strategy_class(notification)

    raise ValueError(f"Unknown notification type: {notification_type}")
