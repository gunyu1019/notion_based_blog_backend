from pydantic import BaseModel, Field, ConfigDict
from pydantic.fields import computed_field

from models.notion.file import File
from .block import Block


class TableBlock(Block):
    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def has_row_header(self) -> bool:
        return self._extra_dict['has_row_header']

    @computed_field
    @property
    def has_column_header(self) -> bool:
        return self._extra_dict['has_column_header']

    @computed_field
    @property
    def width(self) -> int:
        return self._extra_dict['width']

    @computed_field
    @property
    def height(self) -> int:
        if not self.has_children:
            return 0
        return len(self.children)

    class Metadata:
        available_type = ["table"]
