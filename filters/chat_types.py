from typing import List

from aiogram.types import Message
from aiogram.filters import Filter


class ChatTypeFilter(Filter):
    """Filter for checking chat type.
    
    Exapmles:
        - :code:`router.message.filter(ChatTypeFilter(["private"]))`
        - :code:`router.message.filter(ChatTypeFilter(["group", "supergroup"]))`
    """

    def __init__(self, chat_types: List[str]):
        self.chat_types = chat_types


    async def __call__(self, message: Message) -> bool:
        if message.chat.type in self.chat_types:
            return True
        return False
