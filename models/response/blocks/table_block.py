from pydantic import BaseModel, Field, ConfigDict
from pydantic.fields import computed_field

from models.notion.file import File
from .block import Block


class TableBlock(Block):
    has_row_header: bool
    has_column_header: bool
    width: int

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def height(self) -> int:
        if not self.has_children:
            return 0
        return len(self.children)
