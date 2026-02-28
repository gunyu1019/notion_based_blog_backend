from pydantic import ConfigDict, computed_field
from typing import Literal

from .block import Block


class UrlBlock(Block):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    type: Literal["bookmark", "embed", "link_preview"]

    @computed_field
    @property
    def url(self) -> str:
        return self.extra_dict.get('url', "")
