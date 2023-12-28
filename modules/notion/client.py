import aiohttp
from async_client_decorator import *

from models.notion import block


class NotionClient(Session):
    def __init__(self, api_key: str):
        self.api_key = api_key
        super().__init__(
            base_url="https://api.notion.com",
            headers={
                "Authorization": "Bearer {0}".format(self.api_key),
                "Notion-Version": "2022-06-28"
            }
        )

    @get("/v1/blocks/{block_id}/children")
    async def retrieve_block_children(
            self,
            response: aiohttp.ClientResponse,
            block_id: Path | str
    ) -> list[block.BLOCKS]:
        data = await response.json()
        if response.status != 200:
            return

        result = data['results']
        blocks = []
        for raw_block_data in result:
            for T in block.BLOCKS.__args__:
                if T.Meta.type != raw_block_data['type']:
                    continue

                _data = T.model_validate(raw_block_data)
                blocks.append(_data)
                break
        return blocks
