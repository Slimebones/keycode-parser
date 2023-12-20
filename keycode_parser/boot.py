import argparse
from pathlib import Path
from typing import Literal, Self

from keycode_parser.models import PathSource, Source, StdoutSource

class Boot:
    def __init__(
        self,
        input_sources: list[Source],
        output_sources: list[Source]
    ) -> None:
        self._input_sources = input_sources
        self._output_sources = output_sources

    @classmethod
    def from_cli(cls, input_args: list[str], output_args: list[str]) -> Self:
        input_sources = cls._parse_sources(input_args, "input")
        output_sources = cls._parse_sources(output_args, "output")
        return cls(input_sources, output_sources)

    @classmethod
    def _parse_sources(
        cls, raw: list[str], mode: Literal["input", "output"]
    ) -> list[Source]:
        res: list[Source] = []

        for r in raw:
            match r:
                case "@stdout":
                    if mode == "input":
                        raise ValueError(
                            "stdout source cannot appear in input"
                        )

                    res.append(StdoutSource())
                case _:
                    res.append(PathSource(source=Path(r)))

        return res

    async def start(self) -> None:
        for inpsrc in self._input_sources:
            match
        # parser = TypescriptParser(Path(args.path))
        # parsed = await parser.parse()
        # out_dir = Path("var")
        # out_dir.mkdir(parents=True, exist_ok=True)
        # with Path(out_dir, "out.ts").open("w+") as f:
        #     f.write(parsed)

    async _process_input
