"""Capture a child's diagnostic stream."""

import subprocess

result = subprocess.run(
    ["sh", "-c", "printf 'bad note\\n' >&2; exit 2"],
    capture_output=True,
    check=False,
    text=True,
)
print(result.stderr.strip(), result.returncode)
