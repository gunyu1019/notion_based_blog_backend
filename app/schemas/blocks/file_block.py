from pydantic import ConfigDict

from services.notion.models import File
from .block import Block


class FileBlock(Block):
    file: File
    model_config = ConfigDict(from_attributes=True)
