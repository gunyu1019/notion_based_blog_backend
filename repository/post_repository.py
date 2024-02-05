import datetime

from sqlalchemy.orm import selectinload
from sqlalchemy.sql import select, exists
from sqlalchemy.sql.base import NO_ARG

from models.database.block import Block
from models.database.page import Page
from models.notion.block import BLOCKS
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
    def page_model_validate(page_id: str, blocks: list[BLOCKS], last_edited_time: datetime.datetime = NO_ARG) -> Page:
        page_model = Page(id=page_id, last_update_time=last_edited_time)
        page_model.blocks.extend([
            Block.from_block(x, index=i)
            for (i, x) in enumerate(blocks)
        ])
        return page_model

    async def insert_block(
            self,
            page_id: str,
            blocks: list[BLOCKS],
            last_edited_time: datetime.datetime = NO_ARG
    ) -> Page:
        page_model = self.page_model_validate(page_id, blocks, last_edited_time)
        self._session.add(page_model)
        await self._session.commit()
        return page_model

    async def delete_block(self, page_id: str) -> bool:
        origin_block = await self.get_block(page_id)
        await self._session.delete(origin_block)
        await self._session.commit()
        return True

    async def merge_block(self, new_block: Page) -> bool:
        await self._session.merge(new_block)
        await self._session.commit()
        return True
