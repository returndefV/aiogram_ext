from aiogram.types import InputMediaPhoto, InputMediaVideo


class NotificationMedia:

    @staticmethod
    def create_input_media(media_type: str, file_id: str) -> InputMediaPhoto | InputMediaVideo:
        """Creates an InputMedia object based on the type."""

        if media_type == "photo":
            return InputMediaPhoto(type=media_type, media=file_id)

        elif media_type == "video":
            return InputMediaVideo(type=media_type, media=file_id)

        else:
            raise ValueError("Unsupported media type")
