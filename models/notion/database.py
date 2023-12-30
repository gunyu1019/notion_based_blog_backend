import datetime

from typing import Any, Annotated
from typing_extensions import Annotated
from pydantic import PrivateAttr, BaseModel, BeforeValidator
from .convert_multiple_type_emoji_or_file import convert_multiple_type_emoji_or_file
from .database_properties import DatabasePropertyType, DatabasePropertyTypeInfo
from .emoji import Emoji
from .file import File


class Database(BaseModel):
    object: str
    id: str
    created_time: datetime.datetime
    # created_by
    last_edited_time: datetime.datetime
    # last_edited_by
    # parent
    archived: bool
    icon: Annotated[
        Emoji | File | None, BeforeValidator(convert_multiple_type_emoji_or_file)
    ]
    cover: Annotated[
        Emoji | File | None, BeforeValidator(convert_multiple_type_emoji_or_file)
    ]
    _properties: dict[str, dict[str, Any]] = PrivateAttr
    url: str
    public_url: str | None

    # _multiple_type_file_key: list[str] = PrivateAttr(["icon", "cover"])

    def __init__(self, **data):
        super().__init__(**data)
        self._properties = data["properties"]

    @property
    def title(self) -> str:
        property_title_data = [
            _property
            for _property in self._properties.values()
            if _property.get("type") == "title"
        ][0]
        database_property_type_info: DatabasePropertyTypeInfo = getattr(
            DatabasePropertyType, "title", None
        ).value
        return database_property_type_info(property_title_data)

    def property_keys(self):
        return self._properties.keys()

    def property(self, key: str) -> Any:
        property_type = self.property_type(key)
        if hasattr(DatabasePropertyType, property_type) is None:
            return
        database_property_type_info: DatabasePropertyTypeInfo = getattr(
            DatabasePropertyType, property_type, None
        ).value

        data = self._properties[key].get(property_type)
        if database_property_type_info.is_array:
            return [database_property_type_info(x) for x in data]
        return database_property_type_info(data)

    def property_type(self, key: str) -> str:
        return self._properties[key].get("type")

    def property_id(self, key: str) -> str:
        return self._properties[key].get("type")
