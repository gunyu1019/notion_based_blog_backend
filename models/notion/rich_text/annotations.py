from pydantic import BaseModel, PrivateAttr
from modules.notion import colors
from utils.find_enum import find_enum


class Annotations(BaseModel):
    bold: bool = False
    italic: bool = False
    strikethrough: bool = False
    underline: bool = False
    code: bool = False
    _color: str = PrivateAttr

    def __init__(self, **data):
        super().__init__(**data)
        self._color = data.get("color")

    @property
    def background_color(self) -> bool:
        return self._color.endswith("_background")

    @property
    def color(self) -> colors.Colors:
        return find_enum(colors.Colors, self._color)
