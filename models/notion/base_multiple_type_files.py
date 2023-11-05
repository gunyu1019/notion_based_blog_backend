from abc import ABC
from pydantic import BaseModel, PrivateAttr, field_validator
from pydantic.fields import ModelPrivateAttr
from .emoji import Emoji
from .file import File


class BaseMultipleTypeFile(BaseModel, ABC):
    _multiple_type_file_key: ModelPrivateAttr = PrivateAttr([""])

    @classmethod
    @field_validator(
        *(
                [_multiple_type_file_key.default]
                if isinstance(_multiple_type_file_key.default, str)
                else _multiple_type_file_key.default
        ),
        mode="before"
    )
    def convert_multiple_type_emoji_or_file(cls, v: dict[str, str] | None):
        obj_type = v.get("type")
        if obj_type == "emoji":
            return Emoji.model_validate(v)
        elif obj_type in ["file", "external"]:
            return File.model_validate(v)
