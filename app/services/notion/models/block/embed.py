from pydantic import computed_field
from .base_block import BaseBlock


class Embed(BaseBlock):
    @computed_field
    @property
    def url(self) -> str:
        return self._data["url"]

    class Meta:
        type: str = "embed"

    type: str = Meta.type
