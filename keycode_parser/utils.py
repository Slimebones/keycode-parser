from pykit.cls import Static


class CodeUtils(Static):
    @staticmethod
    def parse_map_from_codes(codes: list[str]) -> dict[str, dict]:
        res = {}

        for c in codes:
            parts = c.split(".")
            res[parts[0]][parts[1]][parts[2]][parts[3]][parts[4]] = c

        return res
