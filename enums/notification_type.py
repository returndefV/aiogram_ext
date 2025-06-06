from enum import Enum


class NotificationType(str, Enum):
    """This object represents the notification type.

    Choose one:

    - `auto_delay`: Sends a self-destructing message.
    - `info`: Sends a message with an inline button.
    - `invalid_input`: Deletes user's last message. Sends a message with an inline button.
    - `invalid_media_group`: Deletes a media group.
    - `start_menu`: Launches the menu.
    - `edit_menu`: Editing the menu.
    - `close_menu`: Closes the menu.
    - `close_notification`: Closes all recent notifications.
    - `dialog`: Deletes the last message of the user and bot. Sends a message with an inline button.
    - `dialog_media`:
        - Deletes the last message of the user and bot. Sends media.
        - Deletes the last message of the user and bot. Sends media with caption.
        - Deletes the last message of the user and bot. Sends media with an inline button.
        - Deletes the last message of the user and bot. Sends media with caption and an inline button.
    - `dialog_media_apart`:
        - Deletes the last message of the user and bot. Sends media and text.
        - Deletes the last message of the user and bot. Sends media with caption and text.
        - Deletes the last message of the user and bot. Sends media and text with an inline button.
        - Deletes the last message of the user and bot. Sends media with caption and text with an inline button.
    - `dialog_media_group`:
        - Deletes the last message of the user and bot. Sends media group.
        - Deletes the last message of the user and bot. Sends media group and and inline button.
        - Deletes the last message of the user and bot. Sends media group and text.
        - Deletes the last message of the user and bot. Sends media group and text with an inline button.
    - `media`:
        - Sends media.
        - Sends media with caption.
        - Sends media with an inline button.
        - Sends media with caption and an inline button.
    - `media_apart`:
        - Sends media and text.
        - Sends media with caption and text.
        - Sends media and text with an inline button.
        - Sends media with caption and text with an inline button.
    - `media_group`:
        - Sends media group.
        - Sends media group and text.
        - Sends media group and text with an inline button.
    """

    AUTO_DELAY = "auto_delay"
    INFO = "info"
    INVALID_INPUT = "invalid_input"
    INVALID_MEDIA_GROUP = "invalid_media_group"
    START_MENU = "start_menu"
    EDIT_MENU = "edit_menu"
    CLOSE_MENU = "exit_menu"
    CLOSE_NOTIFICATION = "close_notification"
    DIALOG = "dialog"
    DIALOG_MEDIA = "dialog_media"
    DIALOG_MEDIA_APART = "dialog_media_apart"
    DIALOG_MEDIA_GROUP = "dialog_media_group"
    MEDIA = "media"
    MEDIA_APART = "media_apart"
    MEDIA_GROUP = "media_group"
