# learning/code/ex-25-per-case-report/per_case_report.py
"""Worked Example 25: Per-Case Report."""  # => co-07: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import NamedTuple  # => co-05: a typed record for one row of the report


class CaseResult(NamedTuple):  # => co-07: one row of the per-case report -- id, verdict, AND why
    case_id: str  # => co-07: which case this row describes
    passed: bool  # => co-07: the pass/fail decision
    reason: str  # => co-05: WHY -- carried straight from the scorer's own Verdict (ex-18)


RESULTS = [  # => co-07: a small, fixed run's worth of per-case results -- three pass, two fail
    CaseResult("case-01", True, "found required fact '15 GB'"),  # => co-07: row 1 -- pass
    CaseResult("case-02", True, "found required fact '200 GB'"),  # => co-07: row 2 -- pass
    CaseResult("case-08", False, "missing required pattern '24-hour'"),  # => co-07: row 3 -- fail, with its own reason
    CaseResult("case-11", False, "expected 'Pro', found no mention of a plan"),  # => co-07: row 4 -- fail, different reason
    CaseResult("case-12", True, "found required fact 'AES-256'"),  # => co-07: row 5 -- pass
]  # => co-07: closes RESULTS


def render_report(results: list[CaseResult]) -> str:  # => co-07: turns the list into one printable, scannable table
    """Render one line per case: id, PASS/FAIL, and its reason."""  # => co-07: documents render_report's contract -- no runtime output, just sets its __doc__
    lines = [f"{r.case_id:<10} {'PASS' if r.passed else 'FAIL':<5} {r.reason}" for r in results]  # => co-07: one row per case
    return "\n".join(lines)  # => co-07: joined into one multi-line report string


if __name__ == "__main__":  # => co-07: entry point -- runs only when this file executes directly, not on import
    report = render_report(RESULTS)  # => co-07: build the whole table in one call
    print(report)  # => co-07: prints the full per-case report
    failing_ids = [r.case_id for r in RESULTS if not r.passed]  # => co-05: which cases need attention, by id
    print(f"Failing cases: {failing_ids}")  # => co-05: prints exactly which cases to open next
    assert failing_ids == ["case-08", "case-11"], "exactly two named cases must fail, with reasons attached"  # => co-05
    print("MATCH: every failure is traceable straight from the report, with no need to re-run anything")  # => co-07
    # => co-07: the pass rate says IF something regressed; the per-case report says exactly WHICH case and WHY
