from pydantic import ConfigDict, computed_field
from typing import Literal

from .block import Block


class CodeBlock(Block):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    type: Literal["code"]

    @computed_field
    @property
    def language(self) -> str:
        return self.extra_dict["language"]
