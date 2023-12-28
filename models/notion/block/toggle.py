from .base_block import BaseBlock
from ..colorable import Colorable


class Toggle(BaseBlock, Colorable):
    def __init__(self, **data):
        super().__init__(**data)
        self._color = self._data.get("color")

    class Meta:
        type: str = "toggle"

    type: str = Meta.type
