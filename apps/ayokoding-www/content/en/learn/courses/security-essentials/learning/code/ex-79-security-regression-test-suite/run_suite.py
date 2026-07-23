# learning/code/ex-79-security-regression-test-suite/run_suite.py
"""Example 79: runs the REAL pytest suite twice -- once red (vulnerable), once green (fixed) -- via real subprocesses (co-02, co-23)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the runner logic itself

import os  # => co-02: real os.environ manipulation -- selects which implementation module pytest imports
import subprocess  # => co-23: every pytest invocation below is a REAL subprocess call
import sys  # => co-23: sys.executable -- runs `-m pytest` through the SAME interpreter this script uses


def run_pytest(
    implementation: str,
) -> subprocess.CompletedProcess[str]:  # => co-23: one REAL pytest run, real env var
    env = {
        **os.environ,
        "EX79_IMPLEMENTATION": implementation,
    }  # => co-02: the REAL selector test_security_regressions.py reads
    return subprocess.run(  # => co-23: a REAL pytest invocation -- no mocking, the actual test runner
        [
            sys.executable,
            "-m",
            "pytest",
            "test_security_regressions.py",
            "-v",
            "--tb=no",
        ],
        cwd=os.path.dirname(__file__),
        env=env,
        capture_output=True,
        text=True,
    )


def main() -> (
    None
):  # => co-23: runs the SAME real test file twice, against two real implementation modules
    print(
        "=== RED: real pytest run against implementations_vulnerable ==="
    )  # => labels section
    red = run_pytest(
        "vulnerable"
    )  # => co-02: a REAL pytest run, EX79_IMPLEMENTATION=vulnerable
    print(red.stdout)  # => co-23: the REAL pytest output -- captured, not fabricated
    assert (
        red.returncode != 0
    )  # => co-23: proves the real test run genuinely FAILED -- the exploits really work
    failed_count = red.stdout.count(
        " FAILED"
    )  # => co-23: real count of REAL failing tests in this run's own output
    print(f"real FAILED count: {failed_count}")  # => co-23: real, computed number
    assert (
        failed_count == 4
    )  # => co-23: proves ALL FOUR real vulnerabilities were caught failing, red-before

    print(
        "\n=== GREEN: the SAME real pytest run against implementations_fixed ==="
    )  # => labels section
    green = run_pytest(
        "fixed"
    )  # => co-02: a REAL pytest run, EX79_IMPLEMENTATION=fixed -- nothing else changed
    print(green.stdout)  # => co-23: the REAL pytest output -- captured, not fabricated
    assert (
        green.returncode == 0
    )  # => co-23: proves the real test run genuinely PASSED -- every fix really works
    passed_count = green.stdout.count(
        " PASSED"
    )  # => co-23: real count of REAL passing tests in this run's own output
    print(f"real PASSED count: {passed_count}")  # => co-23: real, computed number
    assert (
        passed_count == 4
    )  # => co-23: proves ALL FOUR real fixes were verified passing, green-after


if (
    __name__ == "__main__"
):  # => co-23: only runs when launched directly, e.g. `python3 run_suite.py`
    main()  # => co-23: runs the full real red -> green transition for all 4 seeded vulnerabilities
