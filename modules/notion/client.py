from functools import wraps

import aiohttp
from async_client_decorator import *
from models.notion.block import BLOCKS, BLOCKS_KEY
from models.notion.database import Database
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

    @staticmethod
    def __notion_get_result_able(func):
        func.__component_parameter__.response.append("response")
        return func

    @staticmethod
    def __notion_get_result(func):
        @wraps(func)
        async def wrapper(self, response: aiohttp.ClientResponse, *args, **kwargs):
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

            return await func(self, result=result, *args, **kwargs)

        return wrapper

    @staticmethod
    def __notion_result_listable(func):
        @wraps(func)
        async def wrapper(self, result, *args, **kwargs):
            result_list = result["results"]
            return await func(self, result=result_list, *args, **kwargs)

        return wrapper

    @__notion_get_result_able
    @get("/v1/blocks/{block_id}/children", response_parameter=["response"])
    @__notion_get_result
    @__notion_result_listable
    async def retrieve_block_children(
        self, result: list, block_id: Path | str, detail: bool = False
    ) -> list[BLOCKS]:
        blocks = []
        for raw_block_data in result:
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

    @__notion_get_result_able
    @post("/v1/databases/{database_id}/query", response_parameter=["response"])
    @__notion_get_result
    @__notion_result_listable
    async def query_database(
        self, result: list, database_id: str | Path
    ) -> list[Database]:
        pages = []
        for raw_database_data in result:
            _data = Database.model_validate(raw_database_data)
            pages.append(_data)
        return pages
