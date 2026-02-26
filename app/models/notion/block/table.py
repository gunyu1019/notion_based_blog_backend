from pydantic import computed_field

from .base_block import BaseBlock


class Table(BaseBlock):
    @computed_field
    @property
    def width(self) -> int:
        return self._data["table_width"]

    @computed_field
    @property
    def has_column_header(self) -> bool:
        return self._data["has_column_header"]

    @computed_field
    @property
    def has_row_header(self) -> bool:
        return self._data["has_row_header"]

    class Meta:
        type: str = "table"

    type: str = Meta.type
