from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.types import Text

from models.database.base import Base

if TYPE_CHECKING:
    from models.notion.rich_text import RichText as NotionRichText


class RichText(Base):
    __tablename__ = "rich_text"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    index: Mapped[int] = mapped_column(default=-1)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(String(10), nullable=False, default="text")

    # Annotated
    bold: Mapped[bool] = mapped_column(default=False)
    italic: Mapped[bool] = mapped_column(default=False)
    strikethrough: Mapped[bool] = mapped_column(default=False)
    underline: Mapped[bool] = mapped_column(default=False)
    code: Mapped[bool] = mapped_column(default=False)

    # Text Option
    plain_text: Mapped[str] = mapped_column(Text, nullable=True, default=None)
    href: Mapped[str] = mapped_column(Text, nullable=True, default=None)

    parent_id: Mapped[str] = mapped_column(ForeignKey("block.id"))

    @classmethod
    def from_rich_text(cls, rich_text: "NotionRichText", index: int = -1):
        annotated = rich_text.annotations
        return cls(
            text=rich_text.text,
            index=index,
            href=rich_text.href,
            plain_text=rich_text.plain_text,
            bold=annotated.bold,
            italic=annotated.italic,
            strikethrough=annotated.strikethrough,
            underline=annotated.underline,
            code=annotated.code,
        )
