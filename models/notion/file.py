import datetime

from pydantic import BaseModel, PrivateAttr


class File(BaseModel):
    type: str
    _data: dict[str, str] = PrivateAttr

    def __init__(self, **data):
        super().__init__(**data)
        self._data = data.get(self.type)

    @property
    def url(self) -> str:
        return self._data["url"]

    @property
    def expiry_time(self) -> datetime.datetime | None:
        if "expiry_time" not in self._data or self.type == "external":
            return
        return datetime.datetime.fromisoformat(self._data["expiry_time"])
