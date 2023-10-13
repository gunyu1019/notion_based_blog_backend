from .base_block import BaseBlock
from ..rich_text import RichText


class Code(BaseBlock):
    type: str = "code"
    language: str

    @property
    def captions(self) -> list[RichText] | None:
        if "captions" not in self._data.keys():
            return
        return [RichText.model_validate(x) for x in self._data.get("captions", [])]

