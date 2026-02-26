from typing import Literal

from pydantic import BaseModel


class SortEntries(BaseModel):
    property: str
    direction: Literal["ascending", "descending"] = "ascending"

    # timestamp
    timestamp: Literal["created_time", "last_edited_time"] = None
