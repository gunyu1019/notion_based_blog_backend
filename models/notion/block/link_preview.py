from .base_block import BaseBlock


class LinkPreview(BaseBlock):
    @property
    def url(self) -> str:
        return self._data["url"]

    class Meta:
        type: str = "link_preview"

    type: str = Meta.type
