from pydantic import BaseModel, Field, ConfigDict

from .rich_text import RichText


class Block(BaseModel):
    id: str
    type: str
    text: list[RichText] = Field(default_factory=list)
    has_children: bool = Field(default=False)
    children: list["Block"] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
