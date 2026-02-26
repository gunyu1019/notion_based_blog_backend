from .base_block import BaseBlock


class ColumnList(BaseBlock):
    class Meta:
        type: str = "column_list"

    type: str = Meta.type
