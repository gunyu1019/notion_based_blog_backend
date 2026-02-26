from .base_block import BaseBlock


class Paragraph(BaseBlock):
    class Meta:
        type: str = "paragraph"

    type: str = Meta.type
