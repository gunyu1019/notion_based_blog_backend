from abc import ABC

from .emoji import Emoji
from .file import File


class Fileable(ABC):
    @staticmethod
    def convert_multiple_type_emoji_or_file(
        v: dict[str, str] | None
    ) -> Emoji | File | None:
        if v is None or "type" not in v.keys():
            return None

        obj_type = v["type"]
        if obj_type == "emoji":
            return Emoji.model_validate(v)
        elif obj_type in ["file", "external"]:
            return File.model_validate(v)
