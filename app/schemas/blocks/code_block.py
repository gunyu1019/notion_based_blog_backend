from pydantic import ConfigDict, computed_field

from .block import Block


class CodeBlock(Block):
    model_config = ConfigDict(from_attributes=True)

    class Metadata:
        available_type = ["code"]

    @computed_field
    @property
    def language(self) -> str:
        return self._extra_dict["language"]
