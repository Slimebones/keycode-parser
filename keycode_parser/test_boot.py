import sys
from io import StringIO
from unittest.mock import Mock

import pytest
from pykit.func import FuncSpec

from keycode_parser.boot import Boot
from keycode_parser.io import IOUtils


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("inp", "out"),
    (
        (
            (
                "@stdin",
            ),
            (
                "@stdout",
            ),
        ),
    ),
)
async def test_input_output(inp: list[str], out: list[str]):
    if "@stdin" in inp:
        sys.stdin = Mock(return_value=StringIO(
            "@code(\"c.p.m.t.v1\") @code(\"c.p.m.t.v2\")",
        ))

    stdout = await IOUtils.async_capture_stdout(FuncSpec(Boot.from_cli(
        inp, out,
    ).start))

    assert stdout == "c.p.m.t.v1,c.p.m.t.v2"
