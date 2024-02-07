import asyncio
from typing import TypeVar, Generic, Type

T = TypeVar('T')


class SessionCall(Generic[T]):
    def __init__(self, obj: Type[T], after_closing_method_name: str = "close", *args, **kwargs):
        self.object = obj
        self.args = args
        self.kwargs = kwargs

        self.after_closing_method_name = after_closing_method_name

    async def call(self) -> T:
        client = None
        try:
            client = self.object(*self.args, **self.kwargs)
            yield client
        finally:
            if not hasattr(client, self.after_closing_method_name):
                return

            after_closed_method = getattr(client, self.after_closing_method_name)
            if asyncio.iscoroutinefunction(after_closed_method):
                await after_closed_method()
            else:
                after_closed_method()
