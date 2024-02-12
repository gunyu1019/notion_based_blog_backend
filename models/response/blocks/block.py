import uuid

from pydantic import BaseModel, Field, ConfigDict

from models.response.rich_text import RichText


class Block(BaseModel):
    id: uuid.UUID
    type: str

    has_children: bool = Field(default=False)
    children: list["Block"] = Field(default_factory=list)

    text: list[RichText] = Field(default_factory=list)
    is_file_available: bool = Field(default=False)

    model_config = ConfigDict(from_attributes=True)
