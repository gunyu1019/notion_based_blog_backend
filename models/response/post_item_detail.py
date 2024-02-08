from pydantic import ConfigDict, Field

from .blocks.block import Block
from .post_item import PostItem


class PostItemDetail(PostItem):
    content: list[Block] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
