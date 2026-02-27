import uuid

from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.config import get_config
from app.schemas.content import Content
from app.services.notion.models import BaseBlock
from app.services.notion.models import File
from app.services.notion.client import NotionClient
from app.services.notion.exception import NotFound
from app.utils.session_call import SessionCall

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

    if content_block is None:
        return []

    extra_key_set = (
        set(content_block.model_fields_set) | set(content_block.model_computed_fields.keys())
    ) - (
        set(BaseBlock.model_fields.keys())
        | set(BaseBlock.__pydantic_decorators__.computed_fields.keys())
    )

    result = []
    for extra_key in extra_key_set:
        data = getattr(content_block, extra_key)
        if not isinstance(data, File):
            continue
        result.append(
            Content.from_notion(extra_key, data)
        )
    return result


def setup(client: FastAPI, _: async_sessionmaker):
    client.include_router(router)
