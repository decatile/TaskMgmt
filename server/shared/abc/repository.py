from typing import Type
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from .entity import Entity


class Repository[TEntity: Entity, TId]:
    def __init__(self, entity_type: Type[TEntity], session: AsyncSession):
        super().__init__()
        self._session = session
        self._type = entity_type

    async def find(self, key: TId) -> TEntity | None:
        return await self._session.get(self._type, key)

    async def save(self, *instance: TEntity) -> None:
        self._session.add_all(instance)
        await self._session.flush()

    async def delete(self, *key: TId) -> int:
        result = await self._session.execute(
            delete(self._type).where(self._type.id.in_(key))
        )
        return result.rowcount
