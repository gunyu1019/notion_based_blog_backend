import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, AsyncEngine

from config.config import get_config
from models.notion.block import BLOCKS
from models.notion.database import Database
from modules.notion.client import NotionClient
from repository.post_repository import PostRepository

parser = get_config()


async def main(engine: AsyncEngine, factory: async_sessionmaker):
    client = NotionClient(api_key=parser.get("Notion", "api_key"))
    database_id = parser.get("Notion", "database")

    covered_page = []
    try:
        pages: list[Database] = await client.query_database(database_id=database_id)
        for _block in pages:
            page: list[BLOCKS] = await client.retrieve_block_children(
                block_id=str(_block.id), detail=True
            )
            covered_page.append(
                PostRepository.page_model_validate(
                    page_id=_block.id,
                    blocks=page,
                    last_edited_time=_block.last_edited_time,
                )
            )
    finally:
        await client.close()

    async with factory() as session:
        session: AsyncSession
        session.add_all(covered_page)
        await session.commit()
    await engine.dispose()


def setup(engine: AsyncEngine, factory: async_sessionmaker):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(engine, factory))
