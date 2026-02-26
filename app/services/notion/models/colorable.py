from abc import ABC
from pydantic import BaseModel, PrivateAttr
from .colors import Colors
from utils.find_enum import find_enum


class Colorable(BaseModel, ABC):
    _color: str = PrivateAttr

    @property
    def background_color(self) -> bool:
        return self._color.endswith("_background")

    @property
    def color(self) -> Colors:
        return find_enum(Colors, self._color)
