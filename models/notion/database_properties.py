from enum import Enum
from typing import Any, NamedTuple, Callable

from .property import *
from .rich_text import RichText
from .file import File


class DatabasePropertyTypeInfo(NamedTuple):
    type: type
    callable: Callable[..., Any] = None
    is_array: bool = False

    def __call__(self, *args, **kwargs) -> Any:
        if self.callable is None:
            return self.type(*args, **kwargs)
        return self.callable(*args, **kwargs)


class DatabasePropertyType(Enum):
    checkbox = DatabasePropertyTypeInfo(bool)
    # created_by = DatabasePropertyTypeInfo()
    created_time = DatabasePropertyTypeInfo(
        DateProperty, callable=lambda x: DateProperty.model_validate(x)
    )
    date = DatabasePropertyTypeInfo(
        DateProperty, callable=lambda x: DateProperty.model_validate(x)
    )
    email = DatabasePropertyTypeInfo(str)
    files = DatabasePropertyTypeInfo(
        File, callable=lambda x: File.model_validate(x), is_array=True
    )
    # formula = DatabasePropertyTypeInfo()
    # last_edited_by
    last_edited_time = DatabasePropertyTypeInfo(
        DateProperty, callable=lambda x: DateProperty.model_validate(x)
    )
    multi_select = DatabasePropertyTypeInfo(
        MultiSelectProperty,
        callable=lambda x: MultiSelectProperty.model_validate(x),
        is_array=True,
    )
    number = DatabasePropertyTypeInfo(int)
    # people = DatabasePropertyTypeInfo()
    phone_number = DatabasePropertyTypeInfo(str)
    # relation = DatabasePropertyTypeInfo()
    rich_text = DatabasePropertyTypeInfo(
        RichText, callable=lambda x: RichText.model_validate(x), is_array=True
    )
    # rollup = DatabasePropertyTypeInfo()
    select = DatabasePropertyTypeInfo(str, callable=lambda x: x.get("name"))
    status = DatabasePropertyTypeInfo(str, callable=lambda x: x.get("name"))
    title = DatabasePropertyTypeInfo(
        RichText, callable=lambda x: RichText.model_validate(x), is_array=True
    )
    url = DatabasePropertyTypeInfo(str)
