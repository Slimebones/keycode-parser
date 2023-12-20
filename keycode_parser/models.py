from pathlib import Path
from typing import Any
from pydantic import BaseModel as Model


class Source(Model):
    source: Any | None = None


class PathSource(Source):
    source: Path


class StdoutSource(Source):
    source: None = None
