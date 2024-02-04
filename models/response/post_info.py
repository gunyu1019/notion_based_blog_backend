import datetime
from pydantic import BaseModel, Field

from .block import Block
from .category import Category


class PostInfo(BaseModel):
    id: str
    title: str
    category: list[Category] = Field(default_factory=list)
    thumbnail_url: str | None = None
    hits: int = 0
    published_at: datetime.datetime | None = None
    content: list[Block]
