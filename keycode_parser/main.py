import asyncio

from keycode_parser.cli import CLI


def main():
    asyncio.run(CLI.call())


if __name__ == "__main__":
    main()
