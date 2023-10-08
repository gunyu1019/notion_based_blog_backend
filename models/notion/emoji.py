from pydantic import BaseModel, PrivateAttr


class Emoji(BaseModel):
    type: str
    emoji: str

    def __str__(self) -> str:
        return self.emoji
