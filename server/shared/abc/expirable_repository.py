from typing import Callable, Self, Type
from sqlalchemy import delete
from sqlalchemy.sql import ColumnExpressionArgument
from sqlalchemy.ext.asyncio import AsyncSession
from .entity import Entity
from .repository import Repository

class ExpirableRepository[TEntity: Entity, TKey](Repository[TEntity, TKey]):
    def __init__(
        self,
        entity_type: Type[TEntity],
        session: AsyncSession,
        predicate: Callable[[Self], ColumnExpressionArgument[bool]],
    ):
        super().__init__(entity_type, session)
        self._predicate = predicate

    async def cleanup_expired(self):
        result = await self._session.execute(
            delete(self._type).where(self._predicate(self))
        )
        return result.rowcount
