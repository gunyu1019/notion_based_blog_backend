from pydantic import ConfigDict, Field

from .blocks import BLOCKS_RES
from .post_item import PostItem


class PostItemDetail(PostItem):
    content: list[BLOCKS_RES] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
