import sys
from unittest.mock import patch

import pytest

from keycode_parser.boot import Boot


@pytest.mark.asyncio
@pytest.mark.capture_stdout
@pytest.mark.parametrize(
    ("stdin_contract", "stdin_retval", "stdout_contract", "expected_stdout"),
    (
        (
            "txt",
            "c.p.m.t.v1,c.p.m.t.v2",
            "txt",
            "c.p.m.t.v1,c.p.m.t.v2"
        ),
        (
            "py",
            "@code(\"c.p.m.t.v1\") @code(\"c.p.m.t.v2\")",
            "txt",
            "c.p.m.t.v1,c.p.m.t.v2"
        ),
        (
            "ts",
            "@code(\"c.p.m.t.v1\") @code(\"c.p.m.t.v2\")",
            "txt",
            "c.p.m.t.v1,c.p.m.t.v2"
        ),
    ),
)
async def test_stdin_stdout(
    stdin_contract: str,
    stdin_retval: str,
    stdout_contract: str,
    expected_stdout: str
):
    original_stdout_write = sys.stdout.write
    global res

    def stdout_write_mock(s: str) -> int:
        global res
        res = s
        return original_stdout_write(s)

    with patch.object(sys.stdin, "read", return_value=stdin_retval):
        sys.stdout.write = stdout_write_mock
        await Boot.from_cli(
            ["@stdin:" + stdin_contract],
            ["@stdout:" + stdout_contract]
        ).start()

        assert res == expected_stdout
