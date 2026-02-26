from .base_block import BaseBlock


class Column(BaseBlock):
    class Meta:
        type: str = "column"

    type: str = Meta.type
