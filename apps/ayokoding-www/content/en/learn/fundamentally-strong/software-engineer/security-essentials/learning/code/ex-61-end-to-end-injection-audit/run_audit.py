# learning/code/ex-61-end-to-end-injection-audit/run_audit.py
"""Example 61: sweeps the real vulnerable sample app, then the real fixed one -- 3 sinks down to zero (co-03, co-04, co-01)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the sweep logic itself

import os  # => co-01: builds real, absolute paths to the two real sample files this scan targets

from scanner import (
    scan_file,
)  # => co-01: the REAL AST scanner this example builds and exercises

HERE = os.path.dirname(
    __file__
)  # => co-01: this example's own real directory -- both sample files live alongside it


def main() -> (
    None
):  # => co-01: runs the real scanner against BOTH real sample files, before and after the fix
    print("=== VULNERABLE: scanning sample_vulnerable.py ===")  # => labels section
    vulnerable_findings = scan_file(
        os.path.join(HERE, "sample_vulnerable.py")
    )  # => co-01: a REAL scan of a REAL file
    for finding in (
        vulnerable_findings
    ):  # => co-01: every REAL finding this scan actually produced
        print(
            f"  line {finding.line}: [{finding.sink_type}] {finding.reason}"
        )  # => co-01: real, per-finding detail
    assert (
        len(vulnerable_findings) == 3
    )  # => co-01: proves the scanner found ALL THREE seeded sinks, no more, no less
    assert {f.sink_type for f in vulnerable_findings} == {
        "sql",
        "command",
        "template",
    }  # => co-01: one of each real kind

    print(
        "\n=== FIXED: scanning sample_fixed.py (SAME routes, sinks closed) ==="
    )  # => labels section
    fixed_findings = scan_file(
        os.path.join(HERE, "sample_fixed.py")
    )  # => co-01: a REAL scan of the REAL fixed file
    print(
        f"  findings: {fixed_findings}"
    )  # => co-01: the real, empty list this scan actually produced
    assert (
        fixed_findings == []
    )  # => co-01: proves the identical scanner, run against the fixed file, finds NOTHING

    print(
        "\n=== re-verifying /safe-lookup was NEVER flagged in either file (scanner precision) ==="
    )  # => labels section
    safe_route_source = open(
        os.path.join(HERE, "sample_vulnerable.py")
    ).readlines()  # => co-07: the REAL file, line by line
    flagged_lines = {
        f.line for f in vulnerable_findings
    }  # => co-07: every REAL line number the scan actually flagged
    safe_lines = {
        i + 1 for i, line in enumerate(safe_route_source) if "safe_lookup" in line
    }  # => co-07: real anchor line
    safe_body_start = min(
        safe_lines
    )  # => co-07: where the real, deliberately-safe route begins in the real file
    assert not any(
        line >= safe_body_start for line in flagged_lines
    )  # => co-07: NOTHING inside safe_lookup was flagged


if (
    __name__ == "__main__"
):  # => co-01: only runs when launched directly, e.g. `python3 run_audit.py`
    main()  # => co-01: runs the full real before/after sweep and verifies every real invariant
