from pydantic import PrivateAttr, BeforeValidator
from typing_extensions import Annotated

from .base_block import BaseBlock
from ..convert_multiple_type_emoji_or_file import convert_multiple_type_emoji_or_file
from ..file import File as F


class Image(BaseBlock):
    _text_key = PrivateAttr("caption")
    image: Annotated[F, BeforeValidator(convert_multiple_type_emoji_or_file)]

    @property
    def captions(self) -> str | None:
        return self.text

    class Meta:
        type: str = "image"

    type: str = Meta.type
