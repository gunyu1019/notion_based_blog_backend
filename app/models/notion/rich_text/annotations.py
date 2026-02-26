from ..colorable import Colorable


class Annotations(Colorable):
    bold: bool = False
    italic: bool = False
    strikethrough: bool = False
    underline: bool = False
    code: bool = False

    def __init__(self, **data):
        super().__init__(**data)
        self._color = data.get("color")
