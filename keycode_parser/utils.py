import re
from typing import Literal

from pykit.cls import Static

from keycode_parser.regex import Regex
from keycode_parser.sources import (
    FilepathSource,
    Source,
    SourceContract,
    SourceUtils,
    TextIOSource,
)


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
        source: Source,
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
        if source.contract is None:
            raise ValueError(f"{source} should have a contract")

        content: str = SourceUtils.read(source)

        return CodeUtils.search_for_codes_native(source.contract, content)

    @staticmethod
    def search_for_codes_native(
        contract: str,
        content: str
    ) -> list[str]:
        """
        Search for codes - version for the multiprocessing.
        """
        res = []

        for regex in Regex.ByFileExtension[SourceContract(contract)]:
            res.extend([m.group(0) for m in re.finditer(regex, content)])

        return res
