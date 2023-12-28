from .base_block import BaseBlock
from ..colorable import Colorable


class Table(BaseBlock):
    @property
    def width(self) -> int:
        return self._data["table_width"]

    @property
    def has_column_header(self) -> bool:
        return self._data["has_column_header"]

    @property
    def has_row_header(self) -> bool:
        return self._data["has_row_header"]

    class Meta:
        type: str = "table"

    type: str = Meta.type
