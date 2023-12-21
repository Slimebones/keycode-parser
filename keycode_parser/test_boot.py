import sys
from io import StringIO
from unittest.mock import Mock, patch

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
                "@stdin:py",
            ),
            (
                "@stdout",
            ),
        ),
    ),
)
async def test_input_output(inp: list[str], out: list[str]):
    stdin_retval = "@code(\"c.p.m.t.v1\") @code(\"c.p.m.t.v2\")"

    with patch.object(sys.stdin, "read", return_value=stdin_retval):
        stdout = await IOUtils.async_capture_stdout(FuncSpec(Boot.from_cli(
            inp, out,
        ).start))

        assert stdout == "c.p.m.t.v1,c.p.m.t.v2"
