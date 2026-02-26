from pydantic import computed_field, BeforeValidator
from typing_extensions import Annotated

from .base_block import BaseBlock
from ..fileable import Fileable
from ..emoji import Emoji
from ..file import File
from ..rich_text import RichText


class Callout(BaseBlock, Fileable):
    icon: Annotated[
        Emoji | File | None,
        BeforeValidator(Fileable.convert_multiple_type_emoji_or_file),
    ]

    @computed_field
    @property
    def captions(self) -> list[RichText] | None:
        if "caption" not in self._data.keys():
            return
        return self._rich_text_model_validate(self._data["caption"])

    class Meta:
        type: str = "callout"

    type: str = Meta.type
