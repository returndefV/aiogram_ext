from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto, InputMediaVideo


@dataclass
class NotificationContext:
    msg: Optional[str] = None
    media: Optional[Union[InputMediaPhoto, InputMediaVideo, Dict[str, Any]]] = None
    media_caption: Optional[str] = None
    kbd: Optional[InlineKeyboardMarkup] = None
    button_text: Optional[List[List[str]]] = None
    callback_data: Optional[List[List[str]]] = None
    sizes: tuple[int] = (1,)
    media_group_msg_ids: Optional[List[int]] = None
    menu_msg_id: Optional[int] = None
    bot_last_msg_id: Optional[List[int]] = None
    delay_time: int = 1
