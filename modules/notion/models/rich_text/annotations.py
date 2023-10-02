from pydantic import BaseModel, Field
from ... import colors
from utils.find_enum import find_enum


class Annotations(BaseModel):
    bold: bool
    italic: bool
    strikethrough: bool
    underline: bool
    code: bool
    _color: str = Field(..., alias='color')

    @property
    def background_color(self) -> bool:
        return self._color.endswith('_background')

    @property
    def color(self) -> colors.Colors:
        return find_enum(colors.Colors, self._color)
