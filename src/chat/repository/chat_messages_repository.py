from odmantic import query

from src.chat.models import ChatMessage
from src.chat.repository.base_repository import BaseRepository


class ChatMessageRepository(BaseRepository[ChatMessage]):
    model = ChatMessage

    async def get(
        self,
        user_id: int | None = None,
        chat_id: int | None = None,
    ) -> ChatMessage:
        if user_id is None and chat_id is None:
            raise ValueError("Either user_id or chat_id must be provided")
        query_list = []
        if user_id is not None:
            query_list.append(self.model.user_id == user_id)
        if chat_id is not None:
            query_list.append(self.model.chat_id == chat_id)

        return await self._engine.find_one(
            self.model,
            *query_list,
            sort=query.desc(self.model.created_at)
        )

    async def get_all(
        self,
        *,
        user_id: int | None = None,
        chat_id: int | None = None,
        skip: int | None = 0,
        limit: int | None = None,
    ) -> list[ChatMessage]:
        if user_id is None and chat_id is None:
            raise ValueError("Either user_id or chat_id must be provided")
        query_list = []
        if user_id is not None:
            query_list.append(self.model.user_id == user_id)
        if chat_id is not None:
            query_list.append(self.model.chat_id == chat_id)

        return await self._engine.find(
            self.model,
            *query_list,
            sort=query.desc(self.model.created_at),
            skip=skip,
            limit=limit,
        )

    async def get_all_latest(
        self,
        *,
        user_id: int | None = None,
        chat_id: int | None = None,
        skip: int | None = 0,
        limit: int | None = None,
    ) -> list[ChatMessage]:
        if user_id is None and chat_id is None:
            raise ValueError("Either user_id or chat_id must be provided")
        query_list = []
        if user_id is not None:
            query_list.append(self.model.user_id == user_id)
        if chat_id is not None:
            query_list.append(self.model.chat_id == chat_id)

        total = await self._engine.count(
            self.model,
            *query_list,
        )
        skip = total - limit
        if skip < 0:
            skip = 0

        return await self._engine.find(
            self.model,
            *query_list,
            sort=query.asc(self.model.created_at),
            skip=skip,
            limit=limit,
        )
