import datetime
import random
from pydantic import BaseModel, Field

from .category import Category
from .notion.database import Database
from .notion.property import DateProperty, MultiSelectProperty
from .notion.file import File


class PostItem(BaseModel):
    id: str
    title: str
    category: list[Category] = Field(default_factory=list)
    thumbnail_url: str | None = None
    hits: int = 0
    published_at: datetime.datetime | None = None
    last_edited_time: datetime.datetime | None

    @classmethod
    def from_notion(cls, data: Database):
        title = " ".join([x.text for x in data.title])
        category_property: list[MultiSelectProperty] = data.property("Category")
        categories = [
            Category.model_validate(x.model_dump()) for x in category_property
        ]

        thumbnail_property: list[File] = data.property("Thumbnails") or list()
        thumbnail_url = (
            (random.choice(thumbnail_property)).url
            if len(thumbnail_property) > 0
            else None
        )

        hits: int = data.property("Hits") or 0
        published_at_property: DateProperty | None = data.property("Published At")
        published_at: datetime.datetime | None = getattr(
            published_at_property, "start", None
        )

        last_edited_time: datetime.datetime | None = data.property("Last edited time")

        return cls(
            id=data.id,
            title=title,
            category=categories,
            thumbnail_url=thumbnail_url,
            hits=hits,
            published_at=published_at,
            last_edited_time=last_edited_time,
        )
