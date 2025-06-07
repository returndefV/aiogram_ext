from typing import List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class LogConfig(BaseSettings):
    """
    Logger configuration for Telegram.

    valid_levels = ["debug", "info", "warning", "error", "critical"]

    Example .env settings:

        LOG_GROUP_ID=-100123456789
        ADMIN_USERNAMES=["@admin1","@admin2"]
        MODERATOR_USERNAMES=["@moder1]
        NOTIFY_ADMINS_LEVELS=["error","critical"]
        NOTIFY_MODERATORS_LEVELS=["warning"]
    """

    LOG_GROUP_ID: str
    ADMIN_USERNAMES: List[str] = Field(default_factory=list)
    MODERATOR_USERNAMES: List[str] = Field(default_factory=list)
    NOTIFY_ADMINS_LEVELS: List[str] = Field(default=["error", "critical"])
    NOTIFY_MODERATORS_LEVELS: List[str] = Field(default=["warning"])

    @field_validator('NOTIFY_ADMINS_LEVELS', 'NOTIFY_MODERATORS_LEVELS')
    @classmethod
    def validate_levels(cls, v: List[str]) -> List[str]:
        valid_levels = ["debug", "info", "warning", "error", "critical"]
        for level in v:
            if level not in valid_levels:
                raise ValueError(f"Invalid logging level: {level}")
        return v

    def get_admins_mentions(self) -> str:
        """Generates a line with mentions of admins."""
        return ' '.join(self.ADMIN_USERNAMES) if self.ADMIN_USERNAMES else ''

    def get_moderators_mentions(self) -> str:
        """Generates a line with moderator mentions."""
        return ' '.join(self.MODERATOR_USERNAMES) if self.MODERATOR_USERNAMES else ''

log_config = LogConfig()
