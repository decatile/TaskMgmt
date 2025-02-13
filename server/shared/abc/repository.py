from abc import ABC, abstractmethod
from typing import Type
from sqlalchemy import delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from .entity import Entity


class ABCRepository[TEntity: Entity, TId](ABC):
    @abstractmethod
    def get_class(self) -> Type[TEntity]: ...

    @abstractmethod
    async def find(self, key: TId) -> TEntity | None: ...

    @abstractmethod
    async def save(self, instance: TEntity) -> None: ...

    @abstractmethod
    async def delete(self, *key: TId) -> int: ...


class Repository[TEntity: Entity, TId](ABCRepository[TEntity, TId]):
    def __init__(self, entity_type: Type[TEntity], session: AsyncSession):
        super().__init__()
        self._session = session
        self._type = entity_type

    def get_class(self) -> Type[TEntity]:
        return self._type

    async def find(self, key: TId) -> TEntity | None:
        try:
            return await self._session.get_one(self._type, key)
        except NoResultFound:
            return None

    async def save(self, *instance: TEntity) -> None:
        self._session.add_all(instance)
        await self._session.flush()

    async def delete(self, *key: TId) -> int:
        result = await self._session.execute(
            delete(self._type).where(self._type.id.in_(key))
        )
        return result.rowcount
