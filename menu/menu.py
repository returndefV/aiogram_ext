import logging
from typing import Optional, List, Dict, Tuple, Union

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram_ext.storage.sqlite_storage.models import TableMenu
from aiogram_ext.menu.callback import MenuCallBack

from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

ButtonDict = Dict[str, Union[str, int]]


class Menu:
    def __init__(self, sqlite_session: AsyncSession, bot: Bot):
        self.sqlite_session = sqlite_session
        self.bot = bot

    async def _get_banner_media(
        self,
        name: str,
        text: str,
        banner: Union[bool, str]
    ) -> Optional[InputMediaPhoto]:
        if not banner:
            return None

        try:
            banner_obj = await TableMenu.get_by_menu_name(name, self.sqlite_session)
            if banner_obj and banner_obj.file_id:
                return InputMediaPhoto(media=banner_obj.file_id, caption=banner_obj.text)

            if isinstance(banner, str):
                banner_obj = await TableMenu.store_and_get(
                    path=banner,
                    name=name,
                    text=text,
                    sqlite_session=self.sqlite_session,
                    bot=self.bot
                )
                if banner_obj and banner_obj.file_id:
                    return InputMediaPhoto(media=banner_obj.file_id, caption=banner_obj.text)

        except Exception as e:
            logger.warning(f"Cannot get banner for menu '{name}': {e}")
            return None

    def _build_keyboard(
        self,
        buttons: List[ButtonDict],
        adjust: Tuple[int, ...],
    ) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()

        for btn in buttons:
            if "url" in btn:
                kb.add(InlineKeyboardButton(text=btn["text"], url=btn["url"]))

            elif "callback_data" in btn:
                kb.add(InlineKeyboardButton(text=btn["text"], callback_data=btn["callback_data"]))

            elif "name" in btn:
                cb = MenuCallBack(name=btn["name"]).pack()
                kb.add(InlineKeyboardButton(text=btn["text"], callback_data=cb))

            else:
                raise ValueError(f"Invalid button config: {btn}")

        return kb.adjust(*adjust).as_markup()

    async def create(
        self,
        name: str,
        text: str,
        buttons: List[ButtonDict],
        banner: Union[bool, str] = False,
        adjust: Tuple[int, ...] = (1,),
    ) -> Tuple[Union[str, InputMediaPhoto], InlineKeyboardMarkup]:

        keyboard = self._build_keyboard(buttons, adjust)

        if banner:
            image = await self._get_banner_media(name, text, banner)
            return image, keyboard  # for send_photo
        else:
            return text, keyboard  # for send_message
