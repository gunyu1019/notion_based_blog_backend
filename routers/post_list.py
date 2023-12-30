from fastapi import APIRouter

from config.config import get_config
from models.posts import Posts
from modules.notion.client import NotionClient

parser = get_config()
router = APIRouter()
database_id = parser.get("Notion", "database")
client = NotionClient(
    api_key=parser.get("Notion", "api_key"), version=parser.get("Notion", "version")
)


@router.get("/posts/")
async def list_of_posts():
    pages = await client.query_database(database_id=database_id)
    posts = [[y.text for y in x.title] for x in pages]
    return posts


def setup(app):
    app.include_router(router)
