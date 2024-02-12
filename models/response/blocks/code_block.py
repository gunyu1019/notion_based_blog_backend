from pydantic import BaseModel, Field, ConfigDict, computed_field

from models.notion.file import File
from .block import Block


class CodeBlock(Block):
    model_config = ConfigDict(from_attributes=True)

    class Metadata:
        available_type = ["code"]

    @computed_field
    @property
    def language(self) -> str:
        return self._extra_dict["language"]
