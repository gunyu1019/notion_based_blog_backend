import datetime

from pydantic import BaseModel, Field
from . import rich_text


class Database(BaseModel):
    type: str = Field(..., alias='object')
    id: str
    created_time: datetime.datetime
    # created_by
    last_edited_time: datetime.datetime
    # last_edited_by
    title: list[rich_text.RichText]
    description: list[rich_text.RichText]

