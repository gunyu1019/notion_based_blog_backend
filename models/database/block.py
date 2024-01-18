from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import TYPE_CHECKING

from models.database.base import Base
from models.database.rich_text import RichText


class Block(Base):
    __tablename__ = "block"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    type: Mapped[str] = mapped_column(String(20), nullable=False)

    # Children
    has_children: Mapped[bool] = mapped_column(bool, default=False)
    children: Mapped[list["Block"]] = relationship("Block", remote_side=[id])

    text: Mapped[list[RichText]] = relationship(default_factory=list)
    is_text_available: Mapped[bool] = mapped_column()
    is_file_available: Mapped[bool] = mapped_column(nullable=False)
