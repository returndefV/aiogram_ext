import importlib
import logging
import pkgutil
from typing import Optional, Tuple, Union, List, Dict

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto

from aiogram_ext.menu.menu import Menu

from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class MenuRegistry:
    _registry: dict[str, dict] = {}

    @classmethod
    def register(
        cls,
        name: str,
        text: str,
        buttons: List[Dict],
        banner: Union[bool, str] = False,
        adjust: Tuple[int, ...] = (1,)
    ):
        """Регистрирует меню с заданными параметрами."""

        if not isinstance(name, str) or not name:
            raise ValueError("Name must be non-empty string")

        if not isinstance(buttons, list) or not all(isinstance(btn, dict) for btn in buttons):
            raise ValueError("Buttons must be a list of dicts")

        cls._registry[name] = {
            "text": text,
            "buttons": buttons,
            "banner": banner,
            "adjust": adjust,
        }

    @classmethod
    def auto_discover(cls, package: str):
        """
        Импортирует все модули внутри `package`, чтобы сработали MenuRegistry.register().
        """
        try:
            pkg = importlib.import_module(package)
        except ImportError as e:
            raise ImportError(f"Ошибка импорта пакета '{package}': {e}")

        for _, modname, ispkg in pkgutil.iter_modules(pkg.__path__, prefix=f"{package}."):
            if not ispkg:
                try:
                    importlib.import_module(modname)
                    logger.debug(f"Автоимпортирован модуль меню: {modname}")
                except Exception as e:
                    logger.warning(f"Ошибка импорта модуля {modname}: {e}")

    @classmethod
    async def create(
        cls,
        sqlite_session: AsyncSession,
        bot: Bot,
        name: str
    ) -> Tuple[Optional[InputMediaPhoto], InlineKeyboardMarkup]:
        """Создаёт меню (медиа или сообщение с клавиатурой) по зарегистрированным данным."""

        try:
            data = cls._registry[name]
        except KeyError:
            raise ValueError(f"Menu for name='{name}' not registered.")

        menu = Menu(sqlite_session, bot)
        return await menu.create(
            name=name,
            text=data["text"],
            buttons=data["buttons"],
            banner=data.get("banner", False),
            adjust=data.get("adjust", (1,))
        )
