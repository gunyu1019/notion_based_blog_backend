from pydantic import PrivateAttr

from .base_block import BaseBlock


class Equation(BaseBlock):
    type: str = "equation"
    _text_key = PrivateAttr("expression")

    @property
    def expression(self) -> str:
        return self._data['expression']
