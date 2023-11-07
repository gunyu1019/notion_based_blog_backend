from .base_block import BaseBlock
from ..colorable import Colorable


class NumberedListItem(BaseBlock, Colorable):
    type: str = "numbered_list_item"

    def __init__(self, **data):
        super().__init__(**data)
        self._color = self._data.get("color")

