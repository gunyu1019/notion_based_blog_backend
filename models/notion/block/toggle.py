from .base_block import BaseBlock
from ..colorable import Colorable


class Toggle(BaseBlock, Colorable):
    type: str = "toggle"

    def __init__(self, **data):
        super().__init__(**data)
        self._color = self._data.get("color")
