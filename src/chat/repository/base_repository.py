from typing import Generic, Dict, Any

from odmantic import ObjectId
from odmantic.engine import ModelType, AIOEngine


class BaseRepository(Generic[ModelType]):
    model = None

    def __init__(
        self,
        client,
        *,
        database: str = "public",
    ):
        self._engine = AIOEngine(client=client, database=database)

    @property
    def engine(self):
        return self._engine

    @property
    def session(self):
        return self._engine.session()

    async def create(self, obj: ModelType) -> ModelType:
        created_obj = await self.engine.save(obj)
        return created_obj

    async def create_all(self, objects: list[ModelType]) -> list[ModelType]:
        created_objs = await self.engine.save_all(objects)
        return created_objs

    async def update(self, obj_id: ObjectId, data: Dict[str, Any]) -> ModelType:
        obj = await self.engine.find_one(self.model, ModelType.id == obj_id)
        obj.model_update(data)
        return obj

    async def delete(self, obj_id: ObjectId) -> None:
        obj = await self.engine.find_one(self.model, ModelType.id == obj_id)
        await self.engine.delete(obj)
