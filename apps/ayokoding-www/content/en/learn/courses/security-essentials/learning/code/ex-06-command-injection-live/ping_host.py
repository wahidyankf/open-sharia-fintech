# learning/code/ex-06-command-injection-live/ping_host.py
"""Example 6: Command Injection -- Live."""  # => co-04: module docstring

from __future__ import (
    annotations,
)  # => co-04: DD-39 hygiene, unrelated to the exploit itself

import os  # => co-04: os.system() below hands the WHOLE string to a real shell
import subprocess  # => co-04: subprocess.run([...]) below is the fix -- no shell involved
from pathlib import (
    Path,
)  # => co-04: used to prove/erase the marker file the injected command creates

MARKER = Path(
    "injected_marker.txt"
)  # => co-01: the file an injected command will create if it RUNS


def naive_ping(
    host: str,
) -> int:  # => co-04: the vulnerable handler -- host is tainted (co-01)
    """Ping a host by handing a concatenated string straight to a shell -- VULNERABLE."""  # => co-04: doc
    command = (
        "ping -c 1 " + host
    )  # => co-01: string concatenation -- host is spliced straight into shell text
    print(
        f"COMMAND: {command}"
    )  # => co-04: prints the ACTUAL shell command -- shows the ';' surviving intact
    return os.system(
        command
    )  # => co-04: os.system() ALWAYS runs its argument through /bin/sh -c


def safe_ping(
    host: str,
) -> int:  # => co-04: the FIXED handler -- same tainted host, different execution path
    """Ping a host using an argv list -- FIXED, no shell is ever spawned."""  # => co-04: doc
    args = [
        "ping",
        "-c",
        "1",
        host,
    ]  # => co-04: host is ONE array element, never concatenated into command text
    print(
        f"ARGV: {args!r}"
    )  # => co-04: prints the literal argv -- 'host' is a single opaque argument
    result = subprocess.run(
        args, shell=False, capture_output=True, text=True
    )  # => co-04: shell=False -- NO shell parses this
    print(
        f"STDERR: {result.stderr.strip()}"
    )  # => co-04: ping itself rejects the whole string as an invalid hostname
    return (
        result.returncode
    )  # => co-04: nonzero -- ping failed to resolve the payload as one literal hostname


if (
    __name__ == "__main__"
):  # => co-04: entry point -- legit ping, injection via os.system, then the fix
    MARKER.unlink(
        missing_ok=True
    )  # => co-04: ensure a clean slate -- no leftover marker from a prior run

    print(
        "=== VULNERABLE: legitimate ping ==="
    )  # => co-04: sanity check -- the naive handler works normally
    naive_ping(
        "127.0.0.1"
    )  # => co-04: a real, well-formed hostname -- no shell metacharacters

    print("\n=== VULNERABLE: injected payload ===")  # => co-04: the attack
    payload = "127.0.0.1; touch injected_marker.txt"  # => co-01: ';' chains a SECOND command onto the ping
    naive_ping(
        payload
    )  # => co-04: os.system() runs BOTH commands -- ping, then the injected touch
    print(
        f"marker created by injected command: {MARKER.exists()}"
    )  # => co-04: True -- the injected command RAN

    MARKER.unlink(
        missing_ok=True
    )  # => co-04: reset the marker before testing the fix with the SAME payload
    print(
        "\n=== FIXED: same payload against subprocess.run(shell=False) ==="
    )  # => co-04: re-run against the fix
    safe_ping(
        payload
    )  # => co-01: the SAME string, now treated as one opaque hostname argument
    print(
        f"marker created by injected command: {MARKER.exists()}"
    )  # => co-04: False -- no shell ever parsed the ';'
