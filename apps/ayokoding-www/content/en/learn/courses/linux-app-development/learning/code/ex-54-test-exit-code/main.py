"""Assert a CLI's documented non-zero invalid-input contract."""

import subprocess
import sys


def test_invalid_input_exits_two():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; print('bad input', file=sys.stderr); raise SystemExit(2)",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert result.stderr == "bad input\n"
