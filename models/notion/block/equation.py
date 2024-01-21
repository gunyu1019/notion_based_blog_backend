from pydantic import computed_field, PrivateAttr

from .base_block import BaseBlock


class Equation(BaseBlock):
    @computed_field
    @property
    def expression(self) -> str:
        return self._data["expression"]

    class Meta:
        type: str = "equation"

    type: str = Meta.type
