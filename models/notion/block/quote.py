from .base_block import BaseBlock


class Quote(BaseBlock):
    class Meta:
        type: str = "quote"

    type: str = Meta.type
