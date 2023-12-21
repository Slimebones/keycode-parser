from enum import Enum
from pathlib import Path
from typing import Any, TextIO

from pydantic import BaseModel as Model


class Source(Model):
    source: Any
    contract: str | None = None
    """
    Any string signifies which contract source supports.

    For example, for file source the contract might be file's extension.
    """


class TextIOSource(Source):
    source: TextIO


class FilepathSource(Source):
    source: Path


class SourceContract(Enum):
    TS = "ts"
    JS = "js"
    PY = "py"
