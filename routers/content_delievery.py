import uuid

from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker

from config.config import get_config
from models.response.blocks import *
from models.response.post_item import PostItem
from models.response.post_item_detail import PostItemDetail
from modules.notion.client import NotionClient
from modules.notion.exception import NotFound
from repository.post_repository import PostRepository
from utils.session_call import SessionCall

parser = get_config()
router = APIRouter()
client = SessionCall(
    NotionClient,
    api_key=parser.get("Notion", "api_key"),
    version=parser.get("Notion", "version")
)


@router.get("/content")
async def content(
        item_id: uuid.UUID,
        client_session: NotionClient = Depends(client.call)
):
    try:
        content_block = await client_session.retrieve_block(
            block_id=item_id,
            detail=False
        )
    except NotFound:
        raise HTTPException(status_code=404, detail="Post not found.") 
    content_block
    return 


def setup(client: FastAPI, _db: async_sessionmaker):
    global database
    database.set_factory(_db)
    client.include_router(router)
