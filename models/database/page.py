import datetime

from sqlalchemy import String, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.sql import func

from models.database.base import Base
from models.database.block import Block


class Page(Base):
    __tablename__ = "page"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    short_description: Mapped[str] = mapped_column(Text, nullable=True)
    blocks: Mapped[list[Block]] = relationship(
        "Block", back_populates="page_parent", order_by=Block.index, cascade="all, delete-orphan"
    )

    last_update_time: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), server_onupdate=func.now()
    )
