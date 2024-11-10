from datetime import datetime, UTC
from enum import Enum

from odmantic import Model, Field


class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


def datetime_now_utc():
    return datetime.now(UTC)


class ChatMessage(Model):
    user_id: int
    chat_id: int
    role: Role
    message: str
    created_at: datetime = Field(default_factory=datetime_now_utc)

    model_config = {
        "collection": "chat_messages",
    }
