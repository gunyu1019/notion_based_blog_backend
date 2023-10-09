from pydantic import BaseModel, PrivateAttr
from modules.notion import colors
from utils.find_enum import find_enum


class MultiSelectProperty(BaseModel):
    id: str
    name: str
    _color: str = PrivateAttr

    def __init__(self, **data):
        super().__init__(**data)
        self._color = data.get("color")

    @property
    def color(self) -> colors.Colors:
        return find_enum(colors.Colors, self._color)
