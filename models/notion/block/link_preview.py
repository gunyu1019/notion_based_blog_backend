from .base_block import BaseBlock


class LinkPreview(BaseBlock):
    type: str = "link_preview"

    @property
    def url(self) -> str:
        return self._data['url']
