from pykit.cls import Static

from keycode_parser.sources import SourceContract


class Regex(Static):
    # amount modifiers could be added, but i'm too short of
    # time (i.e. lazy) for that
    Code: str = r"[a-zA-Z-]+\.[a-zA-Z-]+\.[a-zA-Z-]+\.[a-zA-Z-]+\.[a-zA-Z-]+"

    ByFileExtension: dict[SourceContract, list[str]] = {
        SourceContract.PY: [
            r"@code\((" + Code + r")\)",
            r"@legacycode\((" + Code + r")\)",
        ],
    }
