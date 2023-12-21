import typing
from enum import Enum
from io import StringIO, TextIOBase
from pathlib import Path
from typing import Any, Self, TextIO

from pydantic import BaseModel as Model
from pydantic import (
    field_serializer,
    field_validator,
)
from pykit.cls import Static


class Source(Model):
    source: Any
    contract: str
    """
    Any string signifies which contract source supports.

    For example, for file source the contract might be file's extension.
    """

    @classmethod
    def recover(cls, d: dict) -> Self:
        # tmp solution until pykit gets orwynn model support
        d = d.copy()
        t = d.pop("type")

        TargetType: type[Self]

        if t == cls.__name__:
            TargetType = cls
        else:
            TargetType = cls._find_type(t, cls)

        return TargetType.model_validate(d)

    @classmethod
    def _find_type(cls, t: str, ClassType: type[Self]) -> type[Self]:

        subcls = ClassType.__subclasses__()

        if not subcls:
            raise ValueError(f"not class found for type {t}")

        # search outer level first
        for c in subcls:
            if c.__name__ == t:
                return typing.cast(type[Self], c)

        # then search lower level
        for c in subcls:
            return typing.cast(type[Self], cls._find_type(
                t,
                typing.cast(
                    type[Self], c,
                ),
            ))

        raise ValueError

    @property
    def api(self) -> dict:
        # tmp solution until pykit gets orwynn model support
        d = self.model_dump()
        d["type"] = self.__class__.__name__
        return d


class TextIOSource(Source):
    source: TextIOBase

    class Config:
        arbitrary_types_allowed = True

    @field_serializer("source")
    def serialize_source(self, source: TextIO, _info) -> str:
        return source.read()

    @field_validator("source", mode="before")
    @classmethod
    def validate_source(cls, v: TextIO | str) -> TextIO:
        if isinstance(v, TextIO):
            return v
        if isinstance(v, str):
            return StringIO(v)
        raise TypeError


class FilepathSource(Source):
    source: Path


class SourceContract(Enum):
    TXT = "txt"
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
