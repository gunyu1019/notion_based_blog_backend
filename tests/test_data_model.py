import asyncio

from sqlalchemy import select
from sqlalchemy.sql import exists
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection, AsyncEngine
from typing import Callable

from models.database import *


async def main(engine: AsyncEngine, factory: AsyncSession):
    async with engine.begin() as conn:
        conn: AsyncConnection

        await conn.run_sync(Block.metadata.create_all)
        await conn.run_sync(BlockExtra.metadata.create_all)
        await conn.run_sync(Page.metadata.create_all)
        await conn.run_sync(RichText.metadata.create_all)
        await conn.commit()

    async with factory() as session:
        session: AsyncSession

        exists_command = select(exists(Page))
        executed_result = await session.execute(exists_command)

        if not executed_result.scalar_one():
            page = Page(id="1234")
            block = Block(id="1234", type="test", has_children=True)
            children_block = Block(
                id="1235", type="test", has_children=True, page_parent_id=page.id
            )
            sub_children_block = Block(
                id="1236", type="test", has_children=False, page_parent_id=page.id
            )
            text1 = RichText(text="안녕하세요!", color="black")
            text2 = RichText(text="반갑습니다!", color="yellow")

            sub_children_block.text.append(text1)
            sub_children_block.text.append(text2)
            children_block.children.append(sub_children_block)
            block.children.append(children_block)
            page.blocks.append(block)
            session.add(page)
            await session.commit()

        executed_result = await session.execute(
            select(Page).options(selectinload(Page.blocks)).where(Page.id == "1234")
        )
        data = executed_result.scalar_one()
        print(f"Page ID: {data.id}")
        print("-------------------")

        async def block_recursive(block: Block, deep: int = 0):
            print(f"Block ID: {block.id}, deep: {deep}")

            if await block.is_text_available:
                print("Find Text: ", end="")
                for _rich_text in await block.awaitable_attrs.text:
                    print(_rich_text.text, end=" ")
            else:
                print("Find Text: No", end="")
            print()

            if await block.is_extra_available:
                print("Find Extra: ", end="")
                for _extra in await block.awaitable_attrs.extra:
                    print(
                        f"ID={_extra.id} Type={_extra.type}, Value={_extra.data}",
                        end=", ",
                    )
            else:
                print("Find Extra: No", end="")
            print()

            print("-------------------")
            if block.has_children:
                print("Find Children")
                for child_block in await block.awaitable_attrs.children:
                    await block_recursive(child_block, deep + 1)

        for __block in data.blocks:
            await block_recursive(__block)

    await engine.dispose()


def setup(engine: AsyncEngine, factory: AsyncSession):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(engine, factory))
