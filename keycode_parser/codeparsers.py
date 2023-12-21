from keycode_parser.utils import CodeUtils


class CodeParser:
    """
    Parses keycodes in special format.

    This is a base, yet not abstract class. By default it join incoming
    codes with comma in format `<code_1>,<code_2>,<code_3`.
    """
    def __init__(self) -> None:
        pass

    def parse(self, codes: list[str]) -> str:
        return ",".join(codes)


class TypescriptCodeParser(CodeParser):
    _Indentation = 2
    _CodeMaxDepth = 5

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def _get_indentation(cls, modifier: int) -> str:
        return modifier * cls._Indentation * " "

    @classmethod
    def _parse_compatible_code(cls, code: str) -> str:
        return code.replace("-", "_")

    def parse(self, codes: list[str]) -> str:
        return self._parse_map(CodeUtils.parse_map_from_codes(codes))

    def _parse_map(self, map: dict) -> str:
        res = "export default abstract class Codes {\n"

        for k, v in map.items():
            if (not isinstance(v, dict)):
                raise TypeError("company should have subvalues")
            res += self._parse_company(k, v)
            res += "\n"

        res = res.removesuffix("\n")
        res += "};"
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

    def _parse_subcode(  # noqa: PLR0913
        self,
        partcode: str,
        fullcode: str,
        mp: dict,
        indent_modifier: int,
        codedepth: int,
    ) -> str:
        res = \
            self._get_indentation(indent_modifier) \
            + f"{self._parse_compatible_code(partcode)}: "

        if (codedepth < self._CodeMaxDepth):
            res += "{\n"

        if (codedepth == self._CodeMaxDepth):
            res += f"\"{fullcode}\",\n"
        else:
            for k, v in mp.items():
                new_fullcode = fullcode + "." + k
                res += \
                    self._parse_subcode(
                        k, new_fullcode, v, indent_modifier + 1, codedepth + 1,
                    )

        if (codedepth < self._CodeMaxDepth):
            res += self._get_indentation(indent_modifier) + "},\n"

        return res

