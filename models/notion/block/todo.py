from .base_block import BaseBlock
from ..colorable import Colorable


class Todo(BaseBlock, Colorable):
    def __init__(self, **data):
        super().__init__(**data)
        self._color = self._data.get("color")

    @property
    def checked(self):
        return self._data["checked"]

    class Meta:
        type: str = "todo"

    type: str = Meta.type
