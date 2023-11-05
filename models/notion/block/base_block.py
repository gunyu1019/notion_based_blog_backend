import datetime
from abc import ABC
from typing import Any

from pydantic import BaseModel, PrivateAttr
from ..rich_text import RichText


class BaseBlock(BaseModel, ABC):
    object: str
    id: str
    created_time: datetime.datetime
    last_edited_time: datetime.datetime
    has_children: bool
    archived: bool
    type: str
    _data: Any = PrivateAttr()
    _text_key: str = PrivateAttr("rich_text")

    def __init__(self, **data):
        super().__init__(**data)
        self._data = data.get(self.type, {})

    @property
    def text(self) -> list[RichText] | None:
        if self._text_key not in self._data.keys():
            return
        return [RichText.model_validate(x) for x in self._data.get(self._text_key, [])]

    @property
    def is_text(self) -> bool:
        return self.text is None
