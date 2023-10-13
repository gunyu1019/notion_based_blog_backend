from pydantic import PrivateAttr

from .base_block import BaseBlock
from ..base_multiple_type_files import BaseMultipleTypeFile
from ..emoji import Emoji
from ..file import File


class Callout(BaseBlock, BaseMultipleTypeFile):
    type: str = "callout"
    icon: Emoji | File | None

    _text_key = PrivateAttr("captions")
    _multiple_type_file_key = PrivateAttr(["icon"])
