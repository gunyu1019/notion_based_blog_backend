from pydantic import PrivateAttr, BeforeValidator, computed_field
from typing_extensions import Annotated

from .base_block import BaseBlock
from ..convert_multiple_type_emoji_or_file import convert_multiple_type_emoji_or_file
from ..file import File as F
from ..rich_text import RichText


class Image(BaseBlock):
    image: Annotated[F, BeforeValidator(convert_multiple_type_emoji_or_file)]

    @computed_field
    @property
    def captions(self) -> list[RichText] | None:
        if "caption" not in self._data.keys():
            return
        return self._rich_text_model_validate(self._data["caption"])

    class Meta:
        type: str = "image"

    type: str = Meta.type
