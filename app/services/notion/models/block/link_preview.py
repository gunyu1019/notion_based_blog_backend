from pydantic import computed_field

from .base_block import BaseBlock


class LinkPreview(BaseBlock):
    @computed_field
    @property
    def url(self) -> str:
        return self._data["url"]

    class Meta:
        type: str = "link_preview"

    type: str = Meta.type
