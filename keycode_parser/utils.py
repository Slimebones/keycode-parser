import re
import sys
from pykit.cls import Static

from keycode_parser.sources import SourceContract
from keycode_parser.sources import FilepathSource, Source, TextIOSource
from keycode_parser.regex import Regex


class CodeUtils(Static):
    @staticmethod
    def parse_map_from_codes(codes: list[str]) -> dict[str, dict]:
        res = {}

        for c in codes:
            parts = c.split(".")
            res[parts[0]][parts[1]][parts[2]][parts[3]][parts[4]] = c

        return res

    @staticmethod
    def search_for_codes(
        source: Source
    ) -> list[str]:
        """
        Performs searching in the given source for all codes defined by Keycode
        standard.

        Args:
            source:
                Source where to search.
            extension:
                In which extension source's content is.

        Returns:
            List of found codes (could be empty).
        """
        res = []

        if source.contract is None:
            raise ValueError(f"{source} should have a contract")

        content: str
        if isinstance(source, TextIOSource):
            content = source.source.read()
        elif isinstance(source, FilepathSource):
            with source.source.open("r") as f:
                content = f.read()
        else:
            raise TypeError(f"unsupported source {source}")

        for regex in Regex.ByFileExtension[SourceContract(source.contract)]:
            for m in re.finditer(regex, content):
                res.append(m.group(0))

        return res
