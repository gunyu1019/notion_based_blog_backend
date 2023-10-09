import datetime

from abc import ABC
from pydantic import BaseModel, Field


class BaseBlock(BaseModel, ABC):
    object: str
    id: str
    created_time: datetime.datetime
    last_edited_time: datetime.datetime
    has_children: bool
    archived: bool
    type: str
