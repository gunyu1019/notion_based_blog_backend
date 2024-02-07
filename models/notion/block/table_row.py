from pydantic import computed_field

from .base_block import BaseBlock
from ..rich_text import RichText


class TableRow(BaseBlock):
    @computed_field
    @property
    def cells(self) -> list[list[RichText]]:
        cells = self._data["cells"]
        return [
            self._rich_text_model_validate(cell)
            for cell in cells
        ]

    class Meta:
        type: str = "table_row"

    type: str = Meta.type
