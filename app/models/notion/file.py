import datetime

from pydantic import BaseModel, PrivateAttr
from pydantic.fields import computed_field


class File(BaseModel):
    type: str
    _data: dict[str, str] = PrivateAttr

    def __init__(self, **data):
        super().__init__(**data)
        self._data = data.get(self.type)

    @computed_field
    @property
    def url(self) -> str:
        return self._data["url"]

    @computed_field
    @property
    def expiry_time(self) -> datetime.datetime | None:
        if "expiry_time" not in self._data or self.type == "external":
            return
        return datetime.datetime.fromisoformat(self._data["expiry_time"])
