import uuid

from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker

from config.config import get_config
from models.notion.block import BLOCKS
from models.response.blocks import *
from models.response.post_item import PostItem
from models.response.post_item_detail import PostItemDetail
from modules.notion.client import NotionClient
from repository.post_repository import PostRepository
from utils.session_call import SessionCall

parser = get_config()
router = APIRouter()
database_id = parser.get("Notion", "database")
database = PostRepository()
client = SessionCall(
    NotionClient,
    api_key=parser.get("Notion", "api_key"),
    version=parser.get("Notion", "version")
)


@router.get("/posts")
async def list_of_posts(
        private_access: bool = False,
        session: PostRepository = Depends(database.call),
        client_session: NotionClient = Depends(client.call)
):
    pages = await client_session.query_database(database_id=database_id)
    post_items = [
        PostItem.from_notion(x)
        for x in pages
        if not private_access or x.property("Publish") is True
    ]
    pages_from_database = await session.get_pages()
    short_description_with_id = {x.id: x.short_description for x in pages_from_database}
    for post_item in post_items:
        post_item.description = short_description_with_id.get(post_item.id) or "미리보기 없음"
    return post_items


@router.get("/post")
async def post_info(
        post_id: uuid.UUID,
        session: PostRepository = Depends(database.call),
        client_session: NotionClient = Depends(client.call)
):
    page_from_notion = [
        x for x in await client_session.query_database(database_id=database_id)
        if x.id == post_id
    ]
    page_from_database = await session.get_block(page_id=post_id)

    # If notion is not exists, return 404.
    if len(page_from_notion) == 0 or page_from_notion is None:
        raise HTTPException(status_code=404, detail="Post not found.")
    post_item: PostItemDetail = PostItemDetail.from_notion(page_from_notion[0])

    # If database column is not exists, create new column.
    is_new_entry = False
    if page_from_database is None:
        page: list[BLOCKS] = await client_session.retrieve_block_children(
            block_id=post_id,
            detail=True
        )
        page_from_database = await session.insert_block(post_id, page, post_item.last_edited_time)
        is_new_entry = True

    # Equal last edited time (notion == database).
    if post_item.last_edited_time.replace(tzinfo=None) != page_from_database.last_update_time and not is_new_entry:
        page: list[BLOCKS] = await client_session.retrieve_block_children(
            block_id=post_id,
            detail=True
        )
        page_from_database = new_page = session.page_model_validate(post_id, page, post_item.last_edited_time)
        await session.merge_block(new_page)

    post_item.description = page_from_database.short_description
    for _block in page_from_database.blocks:

        for T in BLOCK_RES_SPEC_WITHOUT_RELOAD.__args__:
            if _block.type in T.Metadata.available_type:
                _model = T.model_validate(_block)
                break
        else:
            _model = Block.model_validate(_block)
        _model.set_extra_data(_block.extra_dict)
        post_item.content.append(_model)

    return post_item


def setup(client: FastAPI, _db: async_sessionmaker):
    global database
    database.set_factory(_db)
    client.include_router(router)
