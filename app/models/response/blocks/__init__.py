from .block import Block
from .code_block import CodeBlock
from .file_block import FileBlock
from .table_block import TableBlock
from .url_block import UrlBlock

BLOCK_RES_SPEC_WITHOUT_RELOAD = CodeBlock | TableBlock | UrlBlock
BLOCKS_RES_WITHOUT_RELOAD = BLOCK_RES_SPEC_WITHOUT_RELOAD | Block
BLOCK_SPEC = BLOCK_RES_SPEC_WITHOUT_RELOAD | FileBlock
BLOCKS_RES = BLOCKS_RES_WITHOUT_RELOAD | FileBlock
