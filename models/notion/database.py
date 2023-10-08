import datetime

from typing import Any
from pydantic import BaseModel, Field, PrivateAttr, field_validator
from .database_properties import DatabasePropertyType, DatabasePropertyTypeInfo
from .emoji import Emoji
from .file import File


class Database(BaseModel):
    type: str = Field(..., alias='object')
    id: str
    created_time: datetime.datetime
    # created_by
    last_edited_time: datetime.datetime
    # last_edited_by
    # parent
    archived: bool
    icon: Emoji | File | None
    cover: Emoji | File | None
    _properties: dict[str, dict[str, Any]] = PrivateAttr
    url: str
    public_url: str | None

    def __init__(self, **data):
        super().__init__(**data)
        self._properties = data['properties']

    @classmethod
    @field_validator('icon', 'cover', mode='before')
    def convert_multiple_type_emoji_or_file(cls, v: dict[str, str] | None):
        obj_type = v.get('type')
        if obj_type == 'emoji':
            return Emoji.model_validate(v)
        elif obj_type in ['file', 'external']:
            return File.model_validate(v)

    @property
    def title(self) -> str:
        return self.property('title')

    def property_keys(self):
        return self._properties.keys()

    def property(self, key: str) -> Any:
        property_type = self.property_type(key)
        database_property_type_info: DatabasePropertyTypeInfo = getattr(DatabasePropertyType, property_type, None)
        if database_property_type_info is None:
            return
        database_property_type_info = database_property_type_info.value

        data = self._properties[key].get(property_type)
        if database_property_type_info.is_array:
            return [database_property_type_info(x) for x in data]
        return database_property_type_info(data)

    def property_type(self, key: str) -> str:
        return self._properties[key].get('type')

    def property_id(self, key: str) -> str:
        return self._properties[key].get('type')
