from pydantic import ConfigDict
from pydantic.fields import computed_field
from typing import Literal

from .block import Block


class TableBlock(Block):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    type: Literal["table"]

    @computed_field
    @property
    def has_row_header(self) -> bool:
        return self.extra_dict['has_row_header']

    @computed_field
    @property
    def has_column_header(self) -> bool:
        return self.extra_dict['has_column_header']

    @computed_field
    @property
    def width(self) -> int:
        return self.extra_dict['width']

    @computed_field
    @property
    def height(self) -> int:
        if not self.has_children:
            return 0
        return len(self.children)
