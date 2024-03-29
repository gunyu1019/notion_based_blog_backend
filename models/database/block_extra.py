import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.types import Text

from models.database.base import Base

if TYPE_CHECKING:
    from models.database.block import Block


class BlockExtra(Base):
    __tablename__ = "block_extra"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(10), nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=True, default=None)

    parent: Mapped["Block"] = relationship(back_populates="extra")
    parent_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("block.id", ondelete="CASCADE", onupdate="CASCADE"))
