from typing import Optional
from pydantic_settings import BaseSettings

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


class BotConfig(BaseSettings):
    BOT_TOKEN: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = 'ignore'


class BotManager:
    _bot: Optional[Bot] = None

    @classmethod
    def get_bot(cls) -> Bot:
        """Returns an instance of the bot, initializing it on first call."""

        if cls._bot is not None:
            return cls._bot

        try:
            config = BotConfig()
            cls._bot = Bot(
                token=config.BOT_TOKEN,
                default=DefaultBotProperties(parse_mode=ParseMode.HTML)
            )
            return cls._bot

        except Exception as e:
            raise RuntimeError(f"Bot initialization error: {str(e)}") from e
