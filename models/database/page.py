import datetime

from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import TYPE_CHECKING

from models.database.base import Base
from models.database.block import Block


class Page(Base):
    __tablename__ = "page"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    blocks: Mapped[list[Block]] = relationship()

    last_update_time: Mapped[datetime.datetime] = mapped_column(
        default_factory=datetime.datetime.now
    )
