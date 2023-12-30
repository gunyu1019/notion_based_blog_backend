import datetime

from pydantic import BaseModel, Field


class Posts(BaseModel):
    title: str
    category: list[str] = Field(default_factory=list)
    category_id: list[str] = Field(default_factory=list)
    thumbnail_url: str | None = None
    hits: int = 0
    published_at: datetime.datetime | None = None
