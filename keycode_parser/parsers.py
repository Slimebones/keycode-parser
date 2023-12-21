import json
from pathlib import Path
import re


class TypescriptParser:
    """
    Parses any supported format of structured codes into a typescript object.
    """
    Indentation = 2
    CodeMaxDepth = 5

    def __init__(
        self,
        path: Path
    ) -> None:
        self._path = path

    def parse(self) -> str:
        with self._path.open("r") as f:
            return self._parse_mp(json.load(f))

    @classmethod
    def _get_indentation(cls, modifier: int) -> str:
        return modifier * cls.Indentation * " "

    @classmethod
    def _parse_compatible_code(cls, code: str) -> str:
        return code.replace("-", "_")

    def _parse_mp(self, mp: dict) -> str:
        res = "export default abstract class Codes {\n"

        for k, v in mp.items():
            if (not isinstance(v, dict)):
                raise TypeError("company should have subvalues")
            res += self._parse_company(k, v)
            res += "\n"

        res = res.removesuffix("\n")
        res += "}"
        return res

    def _parse_company(self, company_name: str, mp: dict) -> str:
        res = (
            self._get_indentation(1)
            + "public static"
            + f" {self._parse_compatible_code(company_name.lower())} ="
            + " {\n"
        )

        for k, v in mp.items():
            res += self._parse_subcode(k, company_name + "." + k, v, 2, 2)

        res += self._get_indentation(1) + "};\n"
        return res

    def _parse_subcode(
        self,
        partcode: str,
        fullcode: str,
        mp: dict,
        indent_modifier: int,
        codedepth: int
    ) -> str:
        res = \
            self._get_indentation(indent_modifier) \
            + f"{self._parse_compatible_code(partcode)}: "

        if (codedepth < self.CodeMaxDepth):
            res += "{\n"

        if (codedepth == self.CodeMaxDepth):
            res += f"\"{fullcode}\",\n"
        else:
            for k, v in mp.items():
                new_fullcode = fullcode + "." + k
                res += \
                    self._parse_subcode(
                        k, new_fullcode, v, indent_modifier + 1, codedepth + 1
                    )

        if (codedepth < self.CodeMaxDepth):
            res += self._get_indentation(indent_modifier) + "},\n"

        return res
