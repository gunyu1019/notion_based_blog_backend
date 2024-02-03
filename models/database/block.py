from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from models.database.base import Base
from models.database.block_extra import BlockExtra
from models.database.rich_text import RichText
from models.notion.block.base_block import BaseBlock
from models.notion.fileable import Fileable
from models.notion.file import File

if TYPE_CHECKING:
    from models.database.page import Page
    from models.notion.block import BLOCKS


class Block(Base):
    __tablename__ = "block"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    index: Mapped[int] = mapped_column(Integer, default=-1)
    type: Mapped[str] = mapped_column(String(20), nullable=False)

    page_parent_id: Mapped[str] = mapped_column(ForeignKey("page.id"), nullable=True)
    block_parent_id: Mapped[str] = mapped_column(ForeignKey("block.id"), nullable=True)
    # block_parent: Mapped["Block"] = relationship(back_populates="children")
    block_parent: Mapped["Block"] = relationship(
        "Block",
        remote_side=[id],
        # backref=backref("children", uselist=True, lazy="selectin"),
    )
    page_parent: Mapped["Page"] = relationship(back_populates="blocks")

    # Children
    has_children: Mapped[bool] = mapped_column(default=False)
    # children: Mapped[list["Block"]] = relationship(
    #     "Block",
    #     remote_side=[id],
    #     uselist=True,
    #     backref="block_parent",
    #     lazy="selectin",
    # )
    children: Mapped[list["Block"]] = relationship(
        "Block",
        back_populates="block_parent",
        lazy="selectin",
        uselist=True,
        order_by="Block.index",
    )

    text: Mapped[list[RichText]] = relationship(
        lazy="selectin", order_by=RichText.index
    )
    extra: Mapped[list[BlockExtra]] = relationship(
        back_populates="parent", lazy="selectin"
    )

    is_file_available: Mapped[bool] = mapped_column(nullable=False, default=False)

    @property
    async def is_text_available(self) -> bool:
        return len(await self.awaitable_attrs.text) > 0

    @property
    async def is_extra_available(self) -> bool:
        return len(await self.awaitable_attrs.extra) > 0

    @classmethod
    def from_block(cls, block: "BLOCKS", index: int = -1):
        text = [
            RichText.from_rich_text(x, index=i)
            for (i, x) in enumerate(
                block.text if isinstance(block.text, list) else list()
            )
        ]

        extra_key_set = (
            set(block.model_fields_set) | set(block.model_computed_fields.keys())
        ) - (
            set(BaseBlock.model_fields.keys())
            | set(BaseBlock.__pydantic_decorators__.computed_fields.keys())
        )

        extra = []
        for key in extra_key_set:
            if "captions" == key:
                continue

            data = getattr(block, key)
            _extra_type = "str"
            if isinstance(data, File):
                _extra_type = "file"
                data = None
            _extra = BlockExtra(name=key, value=data, type=_extra_type)
            extra.append(_extra)

        is_file_available = isinstance(block, Fileable)

        children = []
        if block.has_children:
            children = [
                Block.from_block(x, index=i) for i, x in enumerate(block.children)
            ]
        new_cls = cls(
            id=block.id,
            index=index,
            type=block.type,
            is_file_available=is_file_available,
            has_children=block.has_children,
        )
        new_cls.text.extend(text)
        new_cls.extra.extend(extra)
        new_cls.children.extend(children)
        return new_cls
