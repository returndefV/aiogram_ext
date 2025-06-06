from datetime import datetime, timedelta, timezone
from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


class Keyboard:

    @staticmethod
    def generate_key(chat_id: int) -> str:
        timestamp = int(datetime.now(timezone(timedelta())).timestamp())
        return f"{timestamp}{chat_id}"

    @staticmethod
    def constructor_callback_btns(
        button_text: List[List[str]] = None,
        callback_data: List[List[str]] = None,
        btns: dict[str, str] = None,
        key: str = None,
        sizes: tuple[int] = (1,)
    ) -> InlineKeyboardMarkup:
        """Generates an inline keyboard."""

        btns_dict = {}

        if btns is not None:
            btns_dict = btns

        elif button_text is not None and callback_data is not None:
            if len(button_text) != len(callback_data):
                raise ValueError("button_text and callback_data must have the same structure")

            for row_text, row_data in zip(button_text, callback_data):
                if len(row_text) != len(row_data):
                    raise ValueError("Each row in button_text and callback_data must have the same length")

                for text, data in zip(row_text, row_data):
                    final_data = f"{data}_{key}" if data == "delete_notification" else data
                    btns_dict[text] = final_data

        else:
            raise ValueError("Either btns or both button_text and callback_data must be provided.")

        keyboard = InlineKeyboardBuilder()

        for text, data in btns_dict.items():
            keyboard.add(
                InlineKeyboardButton(
                    text=text,
                    callback_data=data,
                )
            )

        return keyboard.adjust(*sizes).as_markup()

    @staticmethod
    def constructor_reply_keyboard(
        *btns: str,
        placeholder: str = None,
        sizes: tuple[int] = (1,)
    ) -> ReplyKeyboardMarkup:
        """Generates an reply keyboard."""

        keyboard = ReplyKeyboardBuilder()

        for text in btns:
            keyboard.add(KeyboardButton(text=text))

        return keyboard.adjust(*sizes).as_markup(resize_keyboard=True, input_field_placeholder=placeholder)
