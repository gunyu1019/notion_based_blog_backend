from pydantic import BaseModel
from .annotations import Annotations


class RichText(BaseModel):
    type: str
    annotations: Annotations
    plain_text: str
    href: None | str
    _text: dict

    def text(self) -> str:
        return self._text['content']

    @property
    def is_redirect(self) -> bool:
        return self.href is not None

    @property
    def redirect(self) -> str:
        return self.href
