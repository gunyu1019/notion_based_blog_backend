from .base_block import BaseBlock


class Embed(BaseBlock):
    type: str = "embed"

    @property
    def url(self) -> str:
        return self._data['url']
