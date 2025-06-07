import asyncio
from enum import Enum
import inspect
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List

from aiogram import Bot

from aiogram_ext.bot.config import BotManager
from aiogram_ext.logger.config import log_config

logger = logging.getLogger(__name__)


class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

VALID_LOG_LEVELS: List[str] = [level.value for level in LogLevel]

@dataclass
class LogEntry:
    text: str
    level: LogLevel
    notify_admins: bool = False
    caller: Optional[str] = None
    chat_id: Optional[int] = None


class TelegramLogger:
    """Asynchronous logger for sending messages to Telegram chat.
    
    Args:
        bot: Telegram bot instance
        chat_id: Chat ID for sending logs
        mention_admins: Mention admins if there are any errors (default: False)
        show_caller: Show call source (default: True)
        rate_limit_seconds: Delay between messages (default: 0.5)
        batch_size: Batch size to send (default: 10)
        max_retries: Maximum number of sending attempts (default: 3)
    """

    def __init__(
        self,
        bot: Bot,
        chat_id: int,
        mention_admins: bool = False,
        show_caller: bool = True,
        rate_limit_seconds: float = 0.5,
        batch_size: int = 10,
        max_retries: int = 3,
    ):
        self.bot = bot
        self.chat_id = chat_id
        self.mention_admins = mention_admins
        self.show_caller = show_caller
        self.rate_limit_seconds = rate_limit_seconds
        self.batch_size = batch_size
        self.max_retries = max_retries

        self.queue = asyncio.Queue()
        self.worker_task: Optional[asyncio.Task] = None
        self._stopping = asyncio.Event()

    async def start(self) -> None:
        """Starts a background worker to process logs."""

        self._stopping.clear()
        self.start_worker()

    async def stop(self) -> None:
        """Stops the background worker and terminates all pending tasks."""

        if self.worker_task:
            self._stopping.set()
            await self.queue.join()
            self.worker_task.cancel()
            try:
                await self.worker_task
            except asyncio.CancelledError:
                pass
            finally:
                logger.info("TelegramLogger background worker has been stopped.")

    def start_worker(self) -> None:
        """Creates and starts a background worker if one is not running."""

        if not self.worker_task or self.worker_task.done():
            self.worker_task = asyncio.create_task(self._worker())
            logger.info("TelegramLogger background worker has been launched.")

    async def _worker(self) -> None:
        """The main loop for processing logs from the queue."""

        while not self._stopping.is_set() or not self.queue.empty():
            batch = await self._get_batch_from_queue()
            await self._process_batch(batch)

    async def _get_batch_from_queue(self) -> List[LogEntry]:
        """Receives a batch of messages from the queue."""

        batch = []
        try:
            for _ in range(self.batch_size):
                log_entry_dict = await asyncio.wait_for(self.queue.get(), timeout=1.0)
                entry = LogEntry(**{
                    **log_entry_dict,
                    "level": LogLevel(log_entry_dict["level"])
                })
                batch.append(entry)
        except (asyncio.TimeoutError, asyncio.CancelledError):
            pass
        return batch

    async def _process_batch(self, batch: List[LogEntry]) -> None:
        """Processes a batch of messages."""

        for entry in batch:
            try:
                await self._send_with_retry(entry)
                await asyncio.sleep(self.rate_limit_seconds)
            except Exception as e:
                logger.exception("Error sending log to Telegram after %d attempts: %s", self.max_retries, e)
            finally:
                self.queue.task_done()

    async def _send_with_retry(self, entry: LogEntry) -> None:
        """Sends a retry message."""

        for attempt in range(self.max_retries):
            try:
                await self._send_to_telegram(entry)
                return
            except Exception:
                if attempt == self.max_retries - 1:
                    raise
                await asyncio.sleep(1 * (attempt + 1))

    async def _send_to_telegram(self, entry: LogEntry) -> None:
        """Sends a formatted message to Telegram."""
        formatted_text = self._format_message(entry)

        try:
            await self.bot.send_message(
                chat_id=entry.chat_id or self.chat_id,
                text=formatted_text
            )
        except Exception as e:
            logger.error("Error sending message in Telegram: '%s'", e)
            raise

    def _format_message(self, entry: LogEntry) -> str:
        """Formats a message for sending in Telegram."""

        parts = [f"<b>{entry.level.upper()}</b>"]

        if self.show_caller and entry.caller:
            parts.append(f"[{entry.caller}]")

        parts.append(f":\n{entry.text}")

        if (entry.level in log_config.NOTIFY_ADMINS_LEVELS or entry.notify_admins) and self.mention_admins:
            admins_mentions = log_config.get_admins_mentions()
            if admins_mentions:
                parts.append(f"\n\n⚠️ {admins_mentions}")

        if entry.level in log_config.NOTIFY_MODERATORS_LEVELS:
            moders_mentions = log_config.get_moderators_mentions()
            if moders_mentions:
                parts.append(f"\n\n👮 {moders_mentions}")

        return "".join(parts)

    def _get_caller_info(self) -> str:
        """Gets information about the calling code."""

        if not self.show_caller:
            return ""

        frame = inspect.currentframe()
        try:
            # Move up 3 frames to skip logger methods
            for _ in range(3):
                if frame:
                    frame = frame.f_back

            if not frame:
                return "unknown"

            code = frame.f_code
            filename = Path(code.co_filename).stem
            func_name = code.co_name

            if 'self' in frame.f_locals:
                class_name = frame.f_locals['self'].__class__.__name__
                return f"{filename}:{class_name}.{func_name}"

            return f"{filename}:{func_name}"
        finally:
            del frame

    async def log(
        self,
        message: str,
        level: LogLevel,
        notify_admins: bool = False,
        chat_id: Optional[int] = None
    ) -> None:
        """The main logging method."""

        if level not in VALID_LOG_LEVELS:
            raise ValueError(f"Invalid logging level: {level}. Valid: {VALID_LOG_LEVELS}")

        caller = self._get_caller_info() if self.show_caller else ""
        full_message = f"[{caller}] {message}" if caller else message
        getattr(logger, level)(full_message)

        await self.queue.put({
            'text': message,
            'level': level,
            'notify_admins': notify_admins,
            'caller': caller,
            'chat_id': chat_id
        })

    async def debug(self, message: str, chat_id: Optional[int] = None) -> None:
        """Logs DEBUG level message."""
        await self.log(message, "debug", chat_id=chat_id)

    async def info(self, message: str, chat_id: Optional[int] = None) -> None:
        """Logs INFO level message."""
        await self.log(message, "info", chat_id=chat_id)

    async def warning(
        self,
        message: str,
        notify_admins: bool = True,
        chat_id: Optional[int] = None
    ) -> None:
        """Logs WARNING level message."""
        await self.log(message, "warning", notify_admins, chat_id)

    async def error(
        self,
        message: str,
        notify_admins: bool = True,
        chat_id: Optional[int] = None
    ) -> None:
        """Logs ERROR level message."""
        await self.log(message, "error", notify_admins, chat_id)

    async def critical(
        self,
        message: str,
        notify_admins: bool = True,
        chat_id: Optional[int] = None
    ) -> None:
        """Logs CRITICAL level message."""
        await self.log(message, "critical", notify_admins, chat_id)


bot = BotManager.get_bot()

telegram_logger = TelegramLogger(
    bot=bot,
    chat_id=log_config.LOG_GROUP_ID,
    mention_admins=True
)
