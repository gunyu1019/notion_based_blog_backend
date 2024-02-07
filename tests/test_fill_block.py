import asyncio
from collections import deque

from sqlalchemy import select, delete
from sqlalchemy.sql import exists
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection, AsyncEngine
from typing import Callable

from config.config import get_config
from models.notion.block import BLOCKS
from models.notion.database import Database
from models.database import *
from modules.notion.client import NotionClient

parser = get_config()


async def main(engine: AsyncEngine, factory: AsyncSession):
    client = NotionClient(api_key=parser.get("Notion", "api_key"))
    database_id = parser.get("Notion", "database")
    covered_page = []
    try:
        pages: list[Database] = await client.query_database(database_id=database_id)
        for _block in pages:
            page: list[BLOCKS] = await client.retrieve_block_children(
                block_id=_block.id, detail=True
            )
            covered_block = Page(id=_block.id)
            covered_block.blocks.extend(
                [Block.from_block(x, index=i) for (i, x) in enumerate(page)]
            )
            print(len(covered_block.blocks))

            block_queue: deque[BLOCKS] = deque(page)
            short_description = ""
            while len(block_queue) > 0:
                if len(short_description) >= 500:
                    break
                _block = block_queue.popleft()
                try:
                    if _block.text is None:
                        continue
                except AttributeError as e:
                    print(_block)
                    raise e
                short_description += " ".join([x.plain_text for x in _block.text if x.plain_text is not None])

                if _block.has_children:
                    block_queue.extendleft(_block.children)
            covered_block.short_description = short_description
            covered_page.append(covered_block)
    finally:
        await client.close()

    async with factory() as session:
        session: AsyncSession
        session.add_all(covered_page)
        await session.commit()
    await engine.dispose()


def setup(engine: AsyncEngine, factory: AsyncSession):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(engine, factory))
