import asyncio
import logging
from datetime import datetime
from typing import AsyncIterable

from aiogram import flags
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from ollama import AsyncClient
from pydantic import BaseModel, ConfigDict

from src.config import config_factory, bot_config_factory
from src.chat.client import get_client_mongodb_connection
from src.chat.models import ChatMessage, Role
from src.chat.repository.chat_messages_repository import ChatMessageRepository

LOG_FORMAT = "%(asctime)s :: %(levelname)-8s :: %(module)s :: %(message)s"

config = config_factory()
mongo_db_client = get_client_mongodb_connection(
    config.mongodb_endpoint,
    config.mongodb_port,
    config.mongodb_admin_login,
    config.mongodb_admin_password,
)
bot, dp = bot_config_factory(config)


class MessageResponse(BaseModel):
    role: str
    content: str


class ModelResponse(BaseModel):
    model: str
    created_at: datetime
    message: MessageResponse
    done: bool

    model_config = ConfigDict(
        extra="ignore",
        arbitrary_types_allowed=True,
        from_attributes=True,
    )


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!")


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    """
    This handler receives messages with `/help` command
    """
    await message.answer(f"Нужна помощь, {hbold(message.from_user.full_name)}?")


async def handle_ollama_response(
    chat_id: int,
) -> AsyncIterable[str]:
    repository = ChatMessageRepository(mongo_db_client)

    messages = [
        MessageResponse(
            role=message.role,
            content=message.message,
        ).model_dump()
        for message in await repository.get_all_latest(
            chat_id=chat_id,
            limit=config.messages_limit,
        )
    ]

    logging.debug(f"messages :: {messages}")
    result = ""

    async for part in await AsyncClient(
        host=config.ollama_endpoint
    ).chat(
        model=config.ollama_model,
        messages=messages,
        stream=True,
        options={**config.ollama_config},
        keep_alive='5m',
    ):
        resp_obj = ModelResponse.model_validate(part)
        logging.debug(f"response obj :: {part}")

        result += resp_obj.message.content

        if resp_obj.done and result:
            yield result
            result = ""

        if "\n" in result:
            yield result
            result = ""


@dp.message()
@flags.chat_action("typing")
async def message_handler(message: Message) -> None:
    repository = ChatMessageRepository(mongo_db_client)

    user_message = await repository.create(
        ChatMessage(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
            message=message.text,
            created_at=message.date,
            role=Role.USER,
        ),
    )
    logging.debug(f"user message :: {user_message}")
    async for response_str in handle_ollama_response(message.chat.id):
        await message.answer(response_str)
        assistant_message = await repository.create(
            ChatMessage(
                user_id=message.from_user.id,
                chat_id=message.chat.id,
                message=response_str,
                role=Role.ASSISTANT,
            ),
        )
        logging.debug(f"assistant message :: {assistant_message}")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG if config.debug else logging.INFO, format=LOG_FORMAT)
    asyncio.run(main())
