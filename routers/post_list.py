from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.ext.asyncio import async_sessionmaker

from config.config import get_config
from models.post_item import PostItem
from modules.notion.client import NotionClient
from repository.post_repository import PostRepository

parser = get_config()
router = APIRouter()
database_id = parser.get("Notion", "database")
database = PostRepository()


@router.get("/posts/")
async def list_of_posts(private_access: bool = False):
    client = NotionClient(
        api_key=parser.get("Notion", "api_key"), version=parser.get("Notion", "version")
    )
    pages = await client.query_database(database_id=database_id)
    await client.close()
    return [
        PostItem.from_notion(x)
        for x in pages
        if not private_access or x.property("published") is True
    ]


@router.get("/post")
async def post_info(post_id: str, session: PostRepository = Depends(database.call)):
    blocks = await session.get_block(page_id=post_id)
    print(blocks.id)
    print(blocks.blocks)
    # print([x for x in blocks.blocks if blocks.id == ])
    print(blocks.blocks[0].children)
    print(blocks.blocks[0].text)
    print(blocks.blocks[0].children[0].has_children)
    print(blocks.blocks[0].children)
    print(blocks.blocks[0].children[0].children[0].children[0].children[0])
    print(blocks.blocks[0].children[0].id)
    print(blocks.blocks[0].id)
    pass


def setup(client: FastAPI, _db: async_sessionmaker):
    global database
    database.set_factory(_db)
    client.include_router(router)
