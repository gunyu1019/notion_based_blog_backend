from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from models.database.base import Base
from models.database.block_extra import BlockExtra
from models.database.rich_text import RichText
from models.notion.block.base_block import BaseBlock
from models.notion.file import File

if TYPE_CHECKING:
    from models.database.page import Page
    from models.notion.block import BLOCKS


class Block(Base):
    __tablename__ = "block"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    type: Mapped[str] = mapped_column(String(20), nullable=False)

    page_parent_id: Mapped[str] = mapped_column(ForeignKey("page.id"), nullable=True)
    block_parent_id: Mapped[str] = mapped_column(ForeignKey("block.id"), nullable=True)
    block_parent: Mapped["Block"] = relationship(back_populates="children")
    page_parent: Mapped["Page"] = relationship(back_populates="blocks")

    # Children
    has_children: Mapped[bool] = mapped_column(default=False)
    children: Mapped[list["Block"]] = relationship(
        "Block", remote_side=[id], back_populates="block_parent", uselist=True
    )

    text: Mapped[list[RichText]] = relationship()
    extra: Mapped[list[BlockExtra]] = relationship(back_populates="parent")

    is_file_available: Mapped[bool] = mapped_column(nullable=False, default=False)

    @property
    async def is_text_available(self) -> bool:
        return len(await self.awaitable_attrs.text) > 0

    @property
    async def is_extra_available(self) -> bool:
        return len(await self.awaitable_attrs.extra) > 0

    @classmethod
    def from_block(cls, block: "BLOCKS"):
        text = [
            RichText.from_rich_text(x)
            for x in (block.text if isinstance(block.text, list) else list())
        ]
        extra_key_set = (
            set(block.model_fields_set) | set(block.model_computed_fields.keys())
        ) - (
            set(BaseBlock.model_fields.keys())
            | set(BaseBlock.__pydantic_decorators__.computed_fields.keys())
        )

        extra = [
            BlockExtra(type=name, data=getattr(block, name)) for name in extra_key_set
        ]
        is_file_available = any(
            [issubclass(File, v1.annotation) for v1 in block.model_fields.values()]
            + [
                issubclass(File, v2.return_type)
                for v2 in block.model_computed_fields.values()
            ]
        )
        return cls(
            id=block.id,
            type=block.type,
            has_children=block.has_children,
            children=block.children,
            text=text,
            is_file_available=is_file_available,
            extra=extra,
        )
