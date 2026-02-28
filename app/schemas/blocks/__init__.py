from .block import Block
from .code_block import CodeBlock
from .file_block import FileBlock
from .table_block import TableBlock
from .url_block import UrlBlock


BLOCK_RES_SPEC_WITHOUT_RELOAD = CodeBlock | TableBlock | UrlBlock
BLOCKS_RES_WITHOUT_RELOAD = BLOCK_RES_SPEC_WITHOUT_RELOAD | Block
BLOCK_SPEC = BLOCK_RES_SPEC_WITHOUT_RELOAD | FileBlock
BLOCKS_RES = BLOCKS_RES_WITHOUT_RELOAD | FileBlock


def _rebuild_models():
    try:
        for block_cls in [Block, CodeBlock, FileBlock, TableBlock, UrlBlock]:
            if hasattr(block_cls, 'model_rebuild'):
                block_cls.model_rebuild(_types_namespace={'AnyBlock': BLOCKS_RES})
    except Exception as _:
        pass

_rebuild_models()
