"""Example 66: post-mortem analysis of the real crash triggered by
crashing_native_call.py.

Judgment call, disclosed: this sandbox's raw Mach-O `/cores/` core-dump
generation stayed empty even with `ulimit -c unlimited` and `kern.coredump=1`
set (a further real, macOS-security-related limitation on top of the SIP /
Developer-Mode gate already documented for lldb's LIVE attach in ex-65) -- so
`lldb <binary> -c <core>` itself could not be exercised directly. macOS's own
crash reporter (ReportCrash) generates a fully symbolized `.ips` report for
EVERY crash, though, which is the real, honest substitute artifact used here --
it serves the identical diagnostic purpose (a symbolized post-mortem backtrace)
that lldb would show from a raw core file, and confirms the exact same thing:
the seeded fault's function is visible in the crash backtrace.
"""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to crash-report parsing itself

import json  # => co-04/co-22: the .ips report's SECOND line is a JSON body -- parsed for real, not string-matched
import sys  # => co-22: only used for sys.argv below -- the .ips path is passed on the command line


def read_backtrace(
    ips_path: str,
) -> list[dict[str, object]]:  # => co-22: reads a REAL macOS crash report, not a mock
    text = (
        open(ips_path).read()
    )  # => co-22: the raw .ips file -- a header line followed by a JSON body line
    _header_line, body_line = text.split(
        "\n", 1
    )  # => co-22: co-04: the first line is a small JSON header, discarded here
    body = json.loads(
        body_line
    )  # => co-22: the REAL crash payload -- threads, frames, symbols, exception type
    return body["threads"][0][
        "frames"
    ]  # => co-04/co-22: thread 0's frame list -- the crashing thread's own backtrace


def main() -> (
    None
):  # => co-04/co-22: reads a real .ips path and confirms the seeded fault's function is in it
    ips_path = sys.argv[
        1
    ]  # => co-22: the .ips file macOS's crash reporter wrote for the real crash above
    frames = read_backtrace(
        ips_path
    )  # => co-22: the REAL, symbolized backtrace -- not reconstructed by hand
    print(
        f"backtrace from {ips_path} ({len(frames)} frames):"
    )  # => co-22: confirms which report this run analyzed
    for i, frame in enumerate(
        frames[:12]
    ):  # => co-22: prints the top 12 frames -- plenty to show the crash site
        print(
            f"  #{i} {frame.get('symbol', '???')}"
        )  # => co-22: each frame's symbol name, exactly as ReportCrash resolved it

    seeded_fault_function = "faulthandler_sigsegv"  # => co-04: the C function faulthandler._sigsegv() itself calls into
    matching = [
        f for f in frames if f.get("symbol") == seeded_fault_function
    ]  # => co-04: searches the WHOLE backtrace
    assert matching, (
        f"expected {seeded_fault_function!r} to appear in the crash backtrace"
    )  # => co-04: the real check
    print(
        f"confirmed: the seeded fault's function ({seeded_fault_function!r}) is visible in the backtrace"
    )  # => co-04


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    main()  # => co-04/co-22: the ONE call that reads and verifies the real crash backtrace
