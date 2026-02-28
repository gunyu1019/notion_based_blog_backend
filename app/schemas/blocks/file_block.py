from pydantic import ConfigDict
from typing import Literal

from app.services.notion.models import File
from .block import Block


class FileBlock(Block):
    file: File
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    type: Literal["file"]
