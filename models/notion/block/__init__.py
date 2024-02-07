from .bookmark import Bookmark
from .bulleted_list_item import BulletedListItem
from .callout import Callout
from .code import Code
from .column_list import ColumnList
from .divider import Divider
from .embed import Embed
from .equation import Equation
from .file import File
from .heading import Heading
from .image import Image
from .link_preview import LinkPreview
from .numbered_list_item import NumberedListItem
from .paragraph import Paragraph
from .pdf import PDF
from .quote import Quote
from .table import Table
from .table_row import TableRow
from .todo import Todo
from .toggle import Toggle
from .video import Video


BLOCKS = (
    Bookmark
    | BulletedListItem
    | Callout
    | Code
    | ColumnList
    | Divider
    | Embed
    | Equation
    | File
    | Heading
    | Image
    | LinkPreview
    | NumberedListItem
    | Paragraph
    | PDF
    | Quote
    | Table
    | TableRow
    | Todo
    | Toggle
    | Video
)
BLOCKS_KEY = {T.Meta.type: T for T in BLOCKS.__args__}
