from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import TYPE_CHECKING

from models.database.base import Base


class RichText(Base):
    __tablename__ = "rich_text"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(65535), nullable=False)

    # Annotated
    bold: Mapped[bool] = mapped_column(default=False)
    italic: Mapped[bool] = mapped_column(default=False)
    strikethrough: Mapped[bool] = mapped_column(default=False)
    underline: Mapped[bool] = mapped_column(default=False)

    # Text Option
    color: Mapped[str] = mapped_column(String(10))
    backgroundColorable: Mapped[bool] = mapped_column(default=False)
    href: Mapped[str] = mapped_column(String(65535), nullable=True, default=None)
