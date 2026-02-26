from pydantic import computed_field

from .base_block import BaseBlock
from ..rich_text import RichText


class Bookmark(BaseBlock):
    @computed_field
    @property
    def url(self) -> str:
        return self._data["url"]

    @computed_field
    @property
    def captions(self) -> list[RichText] | None:
        if "caption" not in self._data.keys():
            return
        return self._rich_text_model_validate(self._data["caption"])

    class Meta:
        type: str = "bookmark"

    type: str = Meta.type
