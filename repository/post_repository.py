import datetime

from collections import deque
from collections.abc import Sequence
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

    async def get_pages(self) -> Sequence[Page]:
        query = (select(Page))
        result = await self._session.execute(query)
        return result.scalars().all()

    @staticmethod
    def page_model_validate(
        page_id: str, blocks: list[BLOCKS], last_edited_time: datetime.datetime = NO_ARG
    ) -> Page:
        page_model = Page(id=page_id, last_update_time=last_edited_time)
        page_model.blocks.extend(
            [Block.from_block(x, index=i) for (i, x) in enumerate(blocks)]
        )

        block_queue: deque[BLOCKS] = deque(blocks)
        short_description = ""
        while len(block_queue) > 0:
            if len(short_description) >= 500:
                break
            block = block_queue.popleft()
            if block.text is None:
                continue
            short_description += " ".join([x.plain_text for x in block.text if x.plain_text is not None])

            if block.has_children:
                block_queue.extendleft(block.children)
        page_model.short_description = short_description
        return page_model

    async def insert_block(
        self,
        page_id: str,
        blocks: list[BLOCKS],
        last_edited_time: datetime.datetime = NO_ARG,
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
