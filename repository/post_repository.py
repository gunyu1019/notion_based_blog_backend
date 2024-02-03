from sqlalchemy.orm import (
    selectinload,
    subqueryload,
    lazyload,
    immediateload,
    joinedload,
    selectin_polymorphic,
)
from sqlalchemy.sql import select

from models.database.page import Page
from models.database.block import Block
from models.database.block_extra import BlockExtra
from models.database.rich_text import RichText
from repository.base_repository import BaseRepository


class PostRepository(BaseRepository):
    async def get_block(self, page_id: str) -> Page:
        query = (
            select(Page)
            .where(Page.id == page_id)
            .options(
                selectinload(Page.blocks),
                selectinload(Page.blocks).selectinload(
                    Block.children, recursion_depth=100
                ),
            )
        )
        result = await self._session.execute(query)
        return result.scalar_one()

    # async def get_meal(
    #         self,
    #         building: list[Building],
    #         date: datetime.date
    # ) -> Sequence[MealInfo]:
    #     query = select(MealInfo).where(MealInfo.date == date).where(MealInfo.building.in_(building))
    #     result = await self._session.execute(query)
    #     return result.scalars().all()
    pass
