from typing import Any

from pydantic import BaseModel, PrivateAttr


class FilterEntries(BaseModel):
    property: str
    property_type: str
    _option = PrivateAttr(default_factory=dict)

    def __init__(self, property: str, property_type: str, **kwargs):
        super().__init__(property=property, property_type=property_type)
        for kw, v in kwargs.items():
            self.add_option(kw, v)

    def add_option(self, key: str, value: Any):
        self._option[key] = value

    def remove_option(self, key: str):
        return self._option.pop(key, None)

    def to_dict(self) -> dict[str, Any]:
        return {"property": self.property, self.property_type: self._option}

    def __contains__(self, item):
        return item in self._option.keys()
