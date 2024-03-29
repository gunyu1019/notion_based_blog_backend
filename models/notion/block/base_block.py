import datetime
import uuid

from abc import ABC
from typing import Any, TYPE_CHECKING
from pydantic import BaseModel, PrivateAttr, Field, computed_field

from ..rich_text import RichText

if TYPE_CHECKING:
    from . import BLOCKS


class BaseBlock(BaseModel, ABC):
    object: str
    id: uuid.UUID
    created_time: datetime.datetime
    last_edited_time: datetime.datetime
    has_children: bool
    archived: bool
    type: str
    _data: Any = PrivateAttr()
    _text_key: str = PrivateAttr("rich_text")
    children: list = Field(default_factory=list)

    def _set_children(self, blocks: list["BLOCKS"]):
        self.children = blocks

    def __init__(self, **data):
        super().__init__(**data)
        self._data = data.get(self.type, {})

    @computed_field
    @property
    def text(self) -> list[RichText] | None:
        if self._text_key not in self._data.keys():
            return
        return self._rich_text_model_validate(self._data.get(self._text_key, None))

    @staticmethod
    def _rich_text_model_validate(
        data: list[dict[str, str | bool]]
    ) -> list[RichText] | None:
        if data is None:
            return
        return [RichText.model_validate(x) for x in data]

    @computed_field
    @property
    def is_text(self) -> bool:
        return self.text is None
