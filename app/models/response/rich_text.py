from pydantic import BaseModel, Field, ConfigDict


class RichText(BaseModel):
    text: str
    type: str

    # Annotated
    bold: bool = Field(default=False)
    italic: bool = Field(default=False)
    strikethrough: bool = Field(default=False)
    underline: bool = Field(default=False)
    code: bool = Field(default=False)

    # Text Option
    plain_text: str | None = Field(default=None)
    href: str | None = Field(default=None)

    model_config = ConfigDict(from_attributes=True)
