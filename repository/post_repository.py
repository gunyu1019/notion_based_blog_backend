from sqlalchemy.orm import selectinload
from sqlalchemy.sql import select, exists

from models.notion.block import BLOCKS
from models.database.block import Block
from models.database.page import Page
from repository.base_repository import BaseRepository


class PostRepository(BaseRepository):
    async def exist_block(self, page_id: str) -> bool:
        query = select(exists(Page).where(Page.id == page_id))
        result = await self._session.execute(query)
        return result.scalar_one_or_none() or False

    async def get_block(self, page_id: str) -> Page | None:
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
        return result.scalar_one_or_none()

    @staticmethod
    def page_model_validate(page_id: str, blocks: list[BLOCKS]) -> Page:
        page_model = Page(id=page_id)
        page_model.blocks.extend([
            Block.from_block(x, index=i)
            for (i, x) in enumerate(blocks)
        ])
        return page_model

    async def insert_block(self, page_id: str, blocks: list[BLOCKS]):
        page_model = self.page_model_validate(page_id, blocks)
        self._session.add(page_model)
        await self._session.commit()

    async def delete_block(self, page_id: str) -> bool:
        origin_block = await self.get_block(page_id)
        await self._session.delete(origin_block)
        await self._session.commit()
        return True

    async def merge_block(self, new_block: Page) -> bool:
        await self._session.merge(new_block)
        await self._session.commit()
        return True
