from fastapi import APIRouter

from config.config import get_config
from models.post_item import PostItem
from modules.notion.client import NotionClient

parser = get_config()
router = APIRouter()
database_id = parser.get("Notion", "database")


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


def setup(app):
    app.include_router(router)
