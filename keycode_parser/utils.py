import re
from typing import Iterable

from pykit.cls import Static

from keycode_parser.regex import Regex
from keycode_parser.sources import (
    Source,
    SourceContract,
    SourceUtils,
)
from pydantic.v1.utils import deep_update


class CodeUtils(Static):
    @staticmethod
    def parse_map_from_codes(codes: Iterable[str]) -> dict[str, dict]:
        res = {}

        for c in codes:
            parts = c.split(".")
            upd = {
                parts[0]: {
                    parts[1]: {
                        parts[2]: {
                            parts[3]: {
                                parts[4]: c
                            },
                        },
                    },
                }
            }
            res = deep_update(res, upd)

        return res

    @staticmethod
    def search_for_codes(
        source: Source | dict,
    ) -> set[str]:
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
        if isinstance(source, dict):
            source = Source.recover(source)

        if source.contract is None:
            raise ValueError(f"{source} should have a contract")

        res = set()
        content: str = SourceUtils.read(source)

        for regex in Regex.InputBySourceContract[
            SourceContract(source.contract)
        ]:
            res.update([m.group(1) for m in re.finditer(regex, content)])

        return res
