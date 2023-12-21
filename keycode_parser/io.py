from contextlib import redirect_stdout
from io import StringIO
from typing import Any, Awaitable, Callable
from pykit.cls import Static
from pykit.func import FuncSpec


class IOUtils(Static):
    @staticmethod
    def capture_stdout(funcspec: FuncSpec) -> str:
        io = StringIO()
        with redirect_stdout(io):
            funcspec.call()
        return io.getvalue()


    # TODO(ryzhovalex): replace with AsyncFunc
    @staticmethod
    async def async_capture_stdout(funcspec: FuncSpec) -> str:
        io = StringIO()
        with redirect_stdout(io):
            funcspec.call()
        return io.getvalue()
