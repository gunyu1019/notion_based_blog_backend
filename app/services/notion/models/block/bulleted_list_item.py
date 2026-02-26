from .base_block import BaseBlock
from ..colorable import Colorable


class BulletedListItem(BaseBlock, Colorable):
    def __init__(self, **data):
        super().__init__(**data)
        self._color = self._data.get("color")

    class Meta:
        type: str = "bulleted_list_item"

    type: str = Meta.type
