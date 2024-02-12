import uuid

from pydantic import BaseModel, Field, ConfigDict, PrivateAttr
from typing import Any

from models.response.rich_text import RichText


class Block(BaseModel):
    id: uuid.UUID
    type: str

    has_children: bool = Field(default=False)
    children: list["Block"] = Field(default_factory=list)

    text: list[RichText] = Field(default_factory=list)
    captions: list[RichText] = Field(default_factory=list)
    is_file_available: bool = Field(default=False)

    _extra_dict: dict[str, Any] = PrivateAttr(default_factory=dict)

    model_config = ConfigDict(from_attributes=True)

    def set_extra_data(self, extra_dict: dict[str, Any]):
        self._extra_dict = extra_dict
