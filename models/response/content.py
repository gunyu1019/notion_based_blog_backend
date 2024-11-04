import datetime
from pydantic import BaseModel

from models.notion.file import File


class Content(BaseModel):
    extra_key: str
    url: str
    expiry_time: datetime.datetime | None

    @classmethod
    def from_notion(cls, key: str, payload: File):
        return cls(
            extra_key=key,
            url=payload.url,
            expiry_time=payload.expiry_time
        )