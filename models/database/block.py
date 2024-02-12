import datetime
import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from models.database.base import Base
from models.database.block_extra import BlockExtra
from models.database.rich_text import RichText
from models.notion.block.base_block import BaseBlock
from models.notion.file import File
from models.notion.fileable import Fileable

if TYPE_CHECKING:
    from models.database.page import Page
    from models.notion.block import BLOCKS, TableRow


class Block(Base):
    __tablename__ = "block"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    index: Mapped[int] = mapped_column(Integer, default=-1)
    type: Mapped[str] = mapped_column(String(20), nullable=False)

    page_parent_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("page.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True
    )
    block_parent_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("block.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True
    )
    # block_parent: Mapped["Block"] = relationship(back_populates="children")
    block_parent: Mapped["Block"] = relationship(
        "Block",
        remote_side=[id],
        cascade="all"
        # backref=backref("children", uselist=True, lazy="selectin"),
    )
    page_parent: Mapped["Page"] = relationship(back_populates="blocks", cascade="all")

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
        cascade="all",
    )

    text: Mapped[list[RichText]] = relationship(
        lazy="selectin",
        order_by=RichText.index,
        cascade="all, delete-orphan",
        primaryjoin="and_(Block.id == RichText.parent_id, RichText.type != 'captions')",
    )
    captions: Mapped[list[RichText]] = relationship(
        lazy="selectin",
        order_by=RichText.index,
        cascade="all, delete-orphan",
        primaryjoin="and_(Block.id == RichText.parent_id, RichText.type == 'captions')",
    )
    extra: Mapped[list[BlockExtra]] = relationship(
        back_populates="parent", lazy="selectin", cascade="all, delete-orphan"
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
            RichText.from_rich_text(
                x,
                index=i,
                _id=uuid.uuid5(block.id, f"block-text-{i}")
            )
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
        captions = []
        for key in extra_key_set:
            # For table-row cells
            if "cells" == key and block.type == "table_row":
                continue

            data = getattr(block, key)

            if "captions" == key:
                captions.extend([
                    RichText.from_rich_text(
                        x,
                        index=i,
                        _type="captions",
                        _id=uuid.uuid5(block.id, f"block-captions-{i}")
                    )
                    for (i, x) in enumerate(data or list())
                ])
                continue
            _extra_type = type(data).__name__
            if isinstance(data, File):
                _extra_type = "file"
                data = None
            _extra = BlockExtra(
                id=uuid.uuid5(block.id, f"block-extra-{key}"),
                name=key,
                value=data,
                type=_extra_type
            )
            extra.append(_extra)

        is_file_available = isinstance(block, Fileable)

        children = []
        if block.has_children:
            children = [
                Block.from_block(x, index=i) for i, x in enumerate(block.children)
            ]

        # For table-row cells
        if block.type == "table_row":
            children.extend(
                [
                    Block.from_notion_table_column(block, index)
                    for index in range(len(block.cells))
                ]
            )

        new_cls = cls(
            id=block.id,
            index=index,
            type=block.type,
            is_file_available=is_file_available,
            has_children=block.has_children,
        )
        new_cls.text.extend(text)
        new_cls.captions.extend(captions)
        new_cls.extra.extend(extra)
        new_cls.children.extend(children)
        return new_cls

    @classmethod
    def from_notion_table_column(
        cls, original_block: "TableRow", index: int
    ) -> "BLOCKS":
        new_uuid = uuid.uuid5(original_block.id, f"table-cell-{index}")

        text = [
            RichText.from_rich_text(x, index=i)
            for (i, x) in enumerate(original_block.cells[index])
        ]

        new_cls = cls(
            id=new_uuid,
            index=index,
            type="table_column",
            is_file_available=False,
            has_children=False,
        )
        new_cls.text.extend(text)
        return new_cls

    @property
    def extra_dict(self) -> dict[str, Any]:
        return {
            x.name: self._extra_tp(x.type)(x.value)
            for x in self.extra
        }

    def get_extra(self, name: str) -> Any:
        return self.extra_dict[name]

    def __contains__(self, item):
        return super().__contains__(item) or item in [p.name for p in self.extra]

    @staticmethod
    def _extra_tp(type_name: str) -> type:
        match type_name:
            case "str":
                return str
            case "int":
                return int
            case "bool":
                return bool
