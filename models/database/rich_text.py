from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.types import Text
from typing import TYPE_CHECKING

from models.database.base import Base

if TYPE_CHECKING:
    from models.database.block import Block


class RichText(Base):
    __tablename__ = "rich_text"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    # Annotated
    bold: Mapped[bool] = mapped_column(default=False)
    italic: Mapped[bool] = mapped_column(default=False)
    strikethrough: Mapped[bool] = mapped_column(default=False)
    underline: Mapped[bool] = mapped_column(default=False)

    # Text Option
    color: Mapped[str] = mapped_column(String(10))
    backgroundColorable: Mapped[bool] = mapped_column(default=False)
    href: Mapped[str] = mapped_column(Text, nullable=True, default=None)

    parent_id: Mapped[str] = mapped_column(ForeignKey("block.id"))
