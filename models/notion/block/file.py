from pydantic import PrivateAttr

from .base_block import BaseBlock
from ..file import File as F
from ..base_multiple_type_files import BaseMultipleTypeFile


class File(BaseBlock, BaseMultipleTypeFile):
    type: str = "file"
    _text_key = PrivateAttr("caption")
    _multiple_type_file_key = PrivateAttr(["file"])
    file: F

    def __init__(self, **data):
        super().__init__(**data)
        self._data = data.get(self.type, {})

    @property
    def captions(self) -> str | None:
        return self.text
