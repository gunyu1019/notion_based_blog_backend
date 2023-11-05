from pydantic import PrivateAttr

from .base_block import BaseBlock


class Heading(BaseBlock):
    type: str = "heading"
    _available_multiple_type_list = PrivateAttr(["heading_1", "heading_2", "heading_3"])

    @property
    def is_toggleable(self) -> bool:
        return self._data['is_toggleable']

    @property
    def heading_type(self) -> int | None:
        if self.type.startswith("heading_"):
            return
        return int(self.type.lstrip("heading_"))
