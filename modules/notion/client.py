from functools import wraps

import aiohttp
from ahttp_client import *
from ahttp_client.extension import multiple_hook

from models.notion.block import BLOCKS, BLOCKS_KEY
from models.notion.database import Database
from models.notion.filter_entries import FilterEntries
from models.notion.sort_entries import SortEntries
from .exception import *


class NotionClient(Session):
    def __init__(self, api_key: str, version: str = "2022-06-28"):
        self.api_key = api_key
        self.version = version

        headers = {"Authorization": self._get_token, "Notion-Version": self.version}

        super().__init__(base_url="https://api.notion.com", headers=headers)

    @property
    def _get_token(self) -> str:
        return "Bearer {0}".format(self.api_key)

    @get("/v1/blocks/{block_id}/children", response_parameter=["response"])
    async def retrieve_block_children(
        self, response: list, block_id: Path | str, detail: bool = False
    ) -> list[BLOCKS]:
        blocks = []
        for raw_block_data in response:
            raw_block_type = raw_block_data["type"]
            if raw_block_type not in BLOCKS_KEY.keys():
                continue

            T = BLOCKS_KEY.get(raw_block_type)
            _data: BLOCKS = T.model_validate(raw_block_data)
            if detail and _data.has_children:
                _data_detail = await self.retrieve_block_children(
                    block_id=_data.id, detail=True
                )
                _data._set_children(_data_detail)
            blocks.append(_data)
        return blocks

    @get("/v1/blocks/{block_id}", response_parameter=["response"])
    async def retrieve_block(
        self, response: dict, block_id: Path | str, detail: bool = False
    ) -> BLOCKS | None:
        raw_block_type = response["type"]
        if raw_block_type not in BLOCKS_KEY.keys():
            return

        T = BLOCKS_KEY.get(raw_block_type)
        block: BLOCKS = T.model_validate(response)
        if detail and block.has_children:
            _data_detail = await self.retrieve_block_children(
                block_id=block.id, detail=True
            )
            block._set_children(_data_detail)
        return block
    
    @post(
        "/v1/databases/{database_id}/query",
        response_parameter=["response"]
    )
    async def query_database(
        self,
        response: list,
        database_id: str | Path,
        filter: FilterEntries | Query = None,
        order_by: list[SortEntries | str] | Query = None,
    ) -> list[Database]:
        pages = []
        for raw_database_data in response:
            _data = Database.model_validate(raw_database_data)
            pages.append(_data)
        return pages

    @query_database.before_hook
    async def __notion_database_query(self, request_obj, path):
        notion_data = dict()
        if "filter" in request_obj.params.keys() and request_obj.params.get("filter") is not None:
            _filter: FilterEntries = request_obj.params.pop("filter")
            notion_data["filter"] = _filter.to_dict()
        if "order_by" in request_obj.params.keys() and request_obj.params.get("order_by") is not None:
            order_by = request_obj.params.pop("order_by")
            if isinstance(order_by, str):
                order_by = SortEntries(property=order_by)
            notion_data["sort"] = order_by.model_dump()
        request_obj.body = notion_data

        if "filter" in request_obj.params.keys():
            request_obj.params.pop("filter")
        if "order_by" in request_obj.params.keys():
            request_obj.params.pop("order_by")
        return request_obj, path
    

    @multiple_hook(retrieve_block_children.after_hook, index=1)
    @multiple_hook(query_database.after_hook, index=1)
    async def __notion_get_result(self, response: aiohttp.ClientResponse):
        data = await response.json()
        status_code = response.status
        if response.status // 100 == 4:
            for E in CLIENT_ERROR_RESPONSE.__args__:
                if E.status_code == status_code:
                    raise E.from_payload(data)
        elif response.status // 100 == 5:
            for E in SERVER_ERROR_RESPONSE.__args__:
                if E.status_code == status_code:
                    raise E()

        result = data
        if data["type"] == "list":
            result = data["result"]

        return [result]
    
    @multiple_hook(retrieve_block_children.after_hook, index=2)
    @multiple_hook(query_database.after_hook, index=2)
    async def __notion_result_listable(self, response):
        result_list = response["results"]
        return result_list