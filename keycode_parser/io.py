from contextlib import redirect_stdout
from io import StringIO
from typing import Any, Awaitable, Callable
from pykit.cls import Static
from pykit.func import FuncSpec


class IOUtils(Static):
    @staticmethod
    def capture_stdout(func: FuncSpec) -> str:
        io = StringIO()
        with redirect_stdout(io):
            func.call()
        return io.getvalue()

    # TODO(ryzhovalex): replace with AsyncFunc
    @staticmethod
    async def async_capture_stdout(func: FuncSpec) -> str:
        io = StringIO()
        with redirect_stdout(io):
            if func.args:
                await func.func(func.args)
            elif func.kwargs:
                await func.func(func.args, **func.kwargs)
            else:
                await func.func()
        return io.getvalue()
