from abc import ABC
from pydantic import BaseModel, PrivateAttr
from modules.notion import colors
from utils.find_enum import find_enum


class Colorable(BaseModel, ABC):
    _color: str = PrivateAttr

    @property
    def background_color(self) -> bool:
        return self._color.endswith("_background")

    @property
    def color(self) -> colors.Colors:
        return find_enum(colors.Colors, self._color)
