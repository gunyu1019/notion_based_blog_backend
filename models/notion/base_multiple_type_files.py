from abc import ABC
from pydantic import BaseModel, PrivateAttr, field_validator
from .emoji import Emoji
from .file import File


class BaseMultipleTypeFile(BaseModel, ABC):
    _multiple_type_file_key: str | list[str] = PrivateAttr

    @classmethod
    @field_validator(
        *([_multiple_type_file_key] if isinstance(_multiple_type_file_key, str) else _multiple_type_file_key),
        mode="before")
    def convert_multiple_type_emoji_or_file(cls, v: dict[str, str] | None):
        obj_type = v.get("type")
        if obj_type == "emoji":
            return Emoji.model_validate(v)
        elif obj_type in ["file", "external"]:
            return File.model_validate(v)
