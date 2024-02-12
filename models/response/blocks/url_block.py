from pydantic import ConfigDict, computed_field

from .block import Block


class UrlBlock(Block):
    model_config = ConfigDict(from_attributes=True)

    class Metadata:
        available_type = ["bookmark", "embed", "link_preview"]

    @computed_field
    @property
    def url(self) -> str:
        return self._extra_dict.get('url', "")
