from pydantic import BaseModel, PrivateAttr
from typing import Any
from .annotations import Annotations


class RichText(BaseModel):
    type: str
    annotations: Annotations
    plain_text: str
    href: None | str
    _text: dict[str, Any] = PrivateAttr

    def __init__(self, **data):
        super().__init__(**data)
        self._text = data.get(self.type, {})

    @property
    def text(self) -> str | None:
        if self.type == "equation":
            return self._text["expression"]
        elif self.type == "text":
            return self._text["content"]
        return

    @property
    def is_redirect(self) -> bool:
        return self.href is not None

    @property
    def redirect(self) -> str:
        return self.href
