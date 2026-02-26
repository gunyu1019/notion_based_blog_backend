from .base_block import BaseBlock


class Divider(BaseBlock):
    class Meta:
        type: str = "divider"

    type: str = Meta.type
