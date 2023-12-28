from pydantic import PrivateAttr

from .base_block import BaseBlock


class Equation(BaseBlock):
    _text_key = PrivateAttr("expression")

    @property
    def expression(self) -> str:
        return self._data["expression"]

    class Meta:
        type: str = "equation"

    type: str = Meta.type
