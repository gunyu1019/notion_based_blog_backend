from __future__ import annotations

import uuid

from pydantic import BaseModel, Field, ConfigDict
from typing import Any, TYPE_CHECKING, ForwardRef

from ..rich_text import RichText


if TYPE_CHECKING:
    from . import BLOCKS_RES as AnyBlock
else:
    AnyBlock = ForwardRef('AnyBlock')


class Block(BaseModel):
    id: uuid.UUID
    type: str

    has_children: bool = Field(default=False)
    children: list[AnyBlock] = Field(default_factory=list)

    text: list[RichText] = Field(default_factory=list)
    captions: list[RichText] = Field(default_factory=list)
    is_file_available: bool = Field(default=False)

    extra_dict: dict[str, Any] = Field(default_factory=dict, exclude=True)

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
