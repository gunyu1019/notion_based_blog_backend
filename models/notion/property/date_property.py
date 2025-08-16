import datetime

from pydantic import BaseModel


class DateProperty(BaseModel):
    start: datetime.datetime
    end: datetime.datetime | None = None
    time_zone: str | None = None
