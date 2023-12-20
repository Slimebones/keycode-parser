import argparse
import sys

from pykit.cls import Static

from keycode_parser.boot import Boot


class CLI(Static):
    @staticmethod
    async def call():
        argparser = argparse.ArgumentParser()
        argparser.add_argument("-i", type=str, nargs="+", dest="input")
        argparser.add_argument("-o", type=str, nargs="+", dest="output")
        args = argparser.parse_args()
        await Boot.from_cli(args.input, args.output).start()
