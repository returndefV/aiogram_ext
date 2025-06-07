from datetime import datetime
import logging
import os
from typing import Optional

from aiogram import Bot

from aiogram.types import FSInputFile

from sqlalchemy import TIMESTAMP, BigInteger, Text, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func

logger = logging.getLogger(__name__)


###################################################################################################
class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models.
    
    An abstract class that defines common fields and behavior for all tables:
        - Auto-incrementing primary key id.
        - Timestamps created (time of creation) and updated (time of last update).
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    c1reated: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())


###################################################################################################
class TableNotificationMessage(Base):
    """Model for storing information about messages (notifications).

    fields:

        - chat_id (int, BigInteger): ID of the chat to which the message(notification) was sent.
        - msg_id (int, BigInteger): message_id of the message(notification) on the telegram servers.
        - key (str): Identification key
    """

    __tablename__ = "table_notification_messages"

    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    msg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    key: Mapped[str] = mapped_column(Text, nullable=False, unique=True)

    @classmethod
    async def save_notification_message_id(
        cls,
        chat_id: int,
        msg_ids: list[int],
        key: str,
        sqlite_session: AsyncSession
    ):
        """Saves multiple IDs of notification-messages."""

        records_to_add = [
            cls(chat_id=chat_id, msg_id=msg_id, key=key)
            for msg_id in msg_ids
        ]
        sqlite_session.add_all(records_to_add)

    @classmethod
    async def get_last_notifications(
        cls,
        chat_id: int,
        sqlite_session: AsyncSession
    ):
        stmt = select(cls.msg_id).where(cls.chat_id == chat_id)
        result = await sqlite_session.execute(stmt)
        records = result.scalars().all()
        return records

    @classmethod
    async def close_last_notifications(
        cls,
        chat_id: int,
        msg_ids: list[int],
        sqlite_session: AsyncSession
    ):
        stmt = delete(cls).where((cls.chat_id == chat_id) & (cls.msg_id.in_(msg_ids)))
        result = await sqlite_session.execute(stmt)
        return result.rowcount > 0

    @classmethod
    async def get_notification_by_key(
        cls,
        key: str,
        sqlite_session: AsyncSession
    ):
        stmt = select(cls).where(cls.key == key)
        result = await sqlite_session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def close_last_notification_by_key(
        cls,
        key: str,
        sqlite_session: AsyncSession
    ):
        stmt = delete(cls).where(cls.key == key)
        result = await sqlite_session.execute(stmt)
        return result.rowcount > 0


###################################################################################################
class TableMenu(Base):
    """Model for storing menu data.

    fields:

        - name (str, unique): Menu name.
        - text (str): Text for message or caption.
        - file_id (str): file_id of the image for the menu on telegram servers.
    """

    __tablename__ = "table_menus"

    name: Mapped[str] = mapped_column(Text, unique=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    file_id: Mapped[str] = mapped_column(Text, nullable=True)

    @classmethod
    async def get_by_menu_name(
        cls,
        name: str,
        sqlite_session: AsyncSession
    ) -> Optional["TableMenu"]:
        """Method for getting menu data by name."""

        stmt = select(cls).where(cls.name == name)
        result = await sqlite_session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def store_and_get(
        cls,
        path: str,
        name: str,
        text: str,
        sqlite_session: AsyncSession,
        bot: Bot
    ) -> Optional["TableMenu"]:
        """The method uploads images for the menu to the telegram servers, then saves its file_id."""

        try:
            banner_file = FSInputFile(path)
            chat_id = os.getenv("MENU_LOG_GROUP_ID") # to send images
            msg = await bot.send_photo(chat_id=chat_id, photo=banner_file, caption=text)
            file_id = msg.photo[-1].file_id

            new_record = cls(name=name, file_id=file_id, text=text)
            sqlite_session.add(new_record)

            return new_record

        except Exception as e:
            logger.error("Error storing banner for '%s' from path '%s': %s", name, path, e)
            return None


###################################################################################################
class TableMenuMessage(Base):
    """Model for storing information about messages (menus).

    fields:

        - chat_id: ID of the chat to which the message(menu) was sent.
        - msg_id: message_id of the message(menu) on the telegram servers.
    """

    __tablename__ = "table_menu_message"

    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    msg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    @classmethod
    async def save_menu_message_id(
        cls,
        chat_id: int,
        msg_ids: list[int],
        sqlite_session: AsyncSession,
    ):
        """Saves multiple IDs of menu-messages."""

        records_to_add = [
            cls(chat_id=chat_id, msg_id=msg_id)
            for msg_id in msg_ids
        ]
        sqlite_session.add_all(records_to_add)

    @classmethod
    async def get_last_menus(
        cls,
        chat_id: int,
        sqlite_session: AsyncSession
    ):
        stmt = select(cls.msg_id).where(cls.chat_id == chat_id)
        result = await sqlite_session.execute(stmt)
        records = result.scalars().all()
        return records

    @classmethod
    async def close_last_menus(
        cls,
        chat_id: int,
        msg_ids: list[int],
        sqlite_session: AsyncSession
    ):
        stmt = delete(cls).where((cls.chat_id == chat_id) & (cls.msg_id.in_(msg_ids)))
        result = await sqlite_session.execute(stmt)
        return result.rowcount > 0
