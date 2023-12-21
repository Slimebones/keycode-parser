import multiprocessing as mp
import argparse
import asyncio
from multiprocessing import Process
from pathlib import Path
from typing import Any, Callable, Literal, Self

import aiofiles
from keycode_parser.types import KeycodeTuple

from keycode_parser.models import PathSource, Source, StdinSource, StdoutSource

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
                case "@stdin":
                    # this could be a default source, since gnu apps generally
                    # do this by default, but to comply with my input-output
                    # source systems, we wanted to make it explicit

                    if mode == "output":
                        raise ValueError(
                            "stdin source cannot appear in input"
                        )
                    res.append(StdinSource())
                case _:
                    res.append(PathSource(source=Path(r)))

        return res

    async def start(self) -> None:
        tuplelist: list[KeycodeTuple] = self._collect_input_sources_map()
        content: str = self._convert_tuplelist_to_content(tuplelist)
        self._write_content_to_output_sources(content)

    def _convert_tuplelist_to_content(
        self, tuplelist: list[KeycodeTuple]
    ) -> str:
        return "stub"

    def _collect_input_sources_map(self) -> list[KeycodeTuple]:
        res: list[KeycodeTuple] = []

        pool_res = []
        pool = mp.Pool()

        for inpsrc in self._input_sources:
            func: Callable
            args: tuple = tuple()

            if isinstance(inpsrc, PathSource):
                func = self._collect_tuple_from_path
                args = (inpsrc.source,)
            elif isinstance(inpsrc, StdinSource):
                func = self._collect_tuple_from_stdin
            else:
                raise ValueError(f"unrecognized input source {inpsrc}")

            pool_res.append(pool.apply(func, args))

        pool.close()
        pool.join()

        for pr in pool_res:
            partial_tuple = pr.get()
            res.update()

        return res

    def _collect_tuple_from_path(self, path: Path) -> KeycodeTuple:
        # parser = TypescriptParser(Path(args.path))
        # parsed = await parser.parse()
        # out_dir = Path("var")
        # out_dir.mkdir(parents=True, exist_ok=True)
        # with Path(out_dir, "out.ts").open("w+") as f:
        #     f.write(parsed)
        return "path", "path", "path", "path", "path"

    def _collect_tuple_from_stdin(self) -> KeycodeTuple:
        return "stdin", "stdin", "stdin", "stdin", "stdin"

    def _write_content_to_output_sources(self, content: str) -> None:
        tasks: list[Process] = []

        for outsrc in self._output_sources:
            if isinstance(outsrc, PathSource):
                tasks.append(asyncio.create_task(
                    self._write_to_output_file(outsrc.source, content)
                ))
            elif isinstance(outsrc, StdoutSource):
                print(content)
            else:
                raise ValueError(f"unrecognized output source {outsrc}")

    def _write_to_output_file(self, path: Path, content: str) -> None:
        # output file is always overwritten, path should be checked before that
        # it is truly an auto file
        with path.open( "w+") as f:
            f.write(content)
