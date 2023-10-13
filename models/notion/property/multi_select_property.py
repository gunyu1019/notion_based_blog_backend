from pydantic import BaseModel, PrivateAttr
from ..colorable import Colorable


class MultiSelectProperty(Colorable):
    id: str
    name: str

    def __init__(self, **data):
        super().__init__(**data)
        self._color = data.get("color")
