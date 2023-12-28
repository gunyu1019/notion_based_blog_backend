from pydantic import PrivateAttr, BeforeValidator
from typing_extensions import Annotated

from .base_block import BaseBlock
from ..convert_multiple_type_emoji_or_file import convert_multiple_type_emoji_or_file
from ..emoji import Emoji
from ..file import File


class Callout(BaseBlock):
    icon: Annotated[Emoji | File | None, BeforeValidator(convert_multiple_type_emoji_or_file)]

    _text_key: str = PrivateAttr("captions")

    class Meta:
        type: str = "callout"

    type: str = Meta.type
