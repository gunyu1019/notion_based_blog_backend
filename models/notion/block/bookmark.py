from pydantic import PrivateAttr
from .base_block import BaseBlock


class Bookmark(BaseBlock):
    type: str = "bookmark"
    _text_key = PrivateAttr("captions")

    @property
    def url(self) -> str:
        return self._data['url']

    @property
    def captions(self) -> str | None:
        return self.text
