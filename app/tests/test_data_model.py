import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncConnection, AsyncEngine

from models import Block, BlockExtra, Page, RichText


async def main(engine: AsyncEngine):
    print("1")
    async with engine.begin() as conn:
        conn: AsyncConnection

        await conn.run_sync(Block.metadata.create_all)
        await conn.run_sync(BlockExtra.metadata.create_all)
        await conn.run_sync(Page.metadata.create_all)
        await conn.run_sync(RichText.metadata.create_all)
        await conn.commit()
    print(2)
    return


def setup(engine: AsyncEngine, factory: async_sessionmaker):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(engine))
