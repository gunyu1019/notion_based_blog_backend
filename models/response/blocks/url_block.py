from pydantic import BaseModel, Field, ConfigDict

from models.notion.file import File
from .block import Block


class UrlBlock(Block):
    url: str
    model_config = ConfigDict(from_attributes=True)
