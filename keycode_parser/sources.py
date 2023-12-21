from enum import Enum
from pathlib import Path
from typing import Any, TextIO
from pykit.cls import Static

from pydantic import BaseModel as Model, ValidationError, validator


class Source(Model):
    source: Any
    contract: str | None = None
    """
    Any string signifies which contract source supports.

    For example, for file source the contract might be file's extension.
    """


class TextIOSource(Source):
    source: TextIO

    class Config:
        arbitrary_types_allowed = True


class FilepathSource(Source):
    source: Path


class SourceContract(Enum):
    TS = "ts"
    JS = "js"
    PY = "py"


class SourceUtils(Static):
    @staticmethod
    def read(source: Source) -> str:
        if isinstance(source, TextIOSource):
            return source.source.read()
        elif isinstance(source, FilepathSource):
            with source.source.open("r") as f:
                return f.read()
        else:
            raise TypeError(f"unsupported source {source}")
