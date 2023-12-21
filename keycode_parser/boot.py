import multiprocessing as mp
from multiprocessing import Process
from pathlib import Path
import sys
from typing import Any, Callable, Literal, Self
from keycode_parser.sources import SourceContract

from keycode_parser.sources import FilepathSource, Source, TextIOSource
from keycode_parser.utils import CodeUtils


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
            if r.startswith("@"):
                res.append(cls._process_special_raw_source(r, mode))
                continue
            res.append(FilepathSource(source=Path(r)))

        return res

    @classmethod
    def _process_special_raw_source(
        cls,
        raw: str,
        mode: Literal["input", "output"]
    ) -> Source:
        """
        Special raw source - starts with "@".
        """
        if raw == "@stdin":
            raise ValueError(
                "specify stdin in format \"@stdin:<extension>\""
            )
        elif raw.startswith("@stdin"):
            if mode == "output":
                raise ValueError(
                    "stdin source cannot appear in output"
                )
            _, raw_extension = raw.split(":")
            contract = SourceContract(raw_extension)
            return TextIOSource(source=sys.stdin, contract=contract.value)
        elif raw == "@stdout":
            if mode == "input":
                raise ValueError(
                    "stdout source cannot appear in input"
                )
            return TextIOSource(source=sys.stdout)
        else:
            raise ValueError(f"unrecognized raw source {raw}")

    async def start(self) -> None:
        codes: list[str] = self._collect_input_sources_map()
        content: str = self._convert_codes_to_content(codes)
        self._write_content_to_output_sources(content)

    def _convert_codes_to_content(
        self,
        codes: list[str]
    ) -> str:
        return "stub"

    def _collect_input_sources_map(self) -> list[str]:
        res: list[str] = []

        pool_res = []
        pool = mp.Pool()

        for source in self._input_sources:
            func: Callable = CodeUtils.search_for_codes
            args: tuple = (source,)

            pool_res.append(pool.apply(func, args))

        pool.close()
        pool.join()

        for pr in pool_res:
            if pr not in res:
                res.append(pr)

        return res

    def _write_content_to_output_sources(self, content: str) -> None:
        processes: list[Process] = []

        for source in self._output_sources:
            if isinstance(source, FilepathSource):
                p = Process(
                    target=self._write_to_output_file,
                    args=(
                        source.source,
                        content
                    )
                )
                p.start()
                processes.append(p)
            elif isinstance(source, TextIOSource):
                source.source.write(content)
            else:
                raise ValueError(f"unrecognized output source {source}")

        for p in processes:
            p.join()

    def _write_to_output_file(self, path: Path, content: str) -> None:
        # output file is always overwritten, path should be checked before that
        # it is truly an auto file
        with path.open( "w+") as f:
            f.write(content)
