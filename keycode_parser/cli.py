import argparse
from pathlib import Path
from keycode_parser.parsers import TypescriptParser


class CLI:
    @staticmethod
    async def call():
        argparser = argparse.ArgumentParser()
        argparser.add_argument("path", type=str)
        argnamespace = argparser.parse_args()
        parser = TypescriptParser(Path(argnamespace.path))
        parsed = await parser.parse()
        out_dir = Path("var")
        out_dir.mkdir(parents=True, exist_ok=True)
        with Path(out_dir, "out.ts").open("w+") as f:
            f.write(parsed)

