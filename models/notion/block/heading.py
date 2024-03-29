from pydantic import computed_field
from .base_block import BaseBlock


class Heading(BaseBlock):
    @computed_field
    @property
    def is_toggleable(self) -> bool:
        return self._data["is_toggleable"]

    @computed_field
    @property
    def heading_type(self) -> int | None:
        if not self.type.startswith("heading_"):
            return
        return int(self.type.lstrip("heading_"))

    class Meta:
        type: str = "heading"
        available_multiple_type_list = ["heading_1", "heading_2", "heading_3"]

    type: str = Meta.type
