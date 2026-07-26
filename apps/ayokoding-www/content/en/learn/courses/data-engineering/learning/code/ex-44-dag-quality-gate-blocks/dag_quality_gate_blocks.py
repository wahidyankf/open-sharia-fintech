"""Worked Example 44: DAG Quality Gate Blocks Downstream."""  # => co-18: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

TASK_LOG: list[str] = []  # => co-18: records exactly which tasks the scheduler actually ran


def extract() -> list[int]:  # => co-18: task 1 -- always runs
    """Extract a batch -- deliberately containing an out-of-range value."""  # => co-18: documents extract's contract -- no runtime output, just sets its __doc__
    TASK_LOG.append("extract")  # => co-18: log this task's participation
    return [10, 20, -5, 30]  # => co-18: -5 is an invalid, out-of-range value (co-16's validity dimension)


def quality_gate(batch: list[int]) -> bool:  # => co-18: task 2 -- the DQ gate task, wired INTO the DAG itself
    """Fail the gate if any value in the batch is negative -- exercises co-16's validity check, from inside the DAG."""  # => co-18: documents quality_gate's contract -- no runtime output, just sets its __doc__
    TASK_LOG.append("quality_gate")  # => co-18: log this task's participation
    return all(value >= 0 for value in batch)  # => co-18: co-16: validity -- every value must be non-negative


def load(batch: list[int]) -> None:  # => co-18: task 3 -- must NEVER run if the gate failed
    """Load the batch -- must be UNREACHABLE whenever the quality gate has failed."""  # => co-18: documents load's contract -- no runtime output, just sets its __doc__
    TASK_LOG.append("load")  # => co-18: log this task's participation -- reached ONLY if the gate passed


if __name__ == "__main__":  # => co-18: entry point -- runs only when this file executes directly, not on import
    batch = extract()  # => co-18: run extract -- ALWAYS the first task in this DAG
    gate_passed = quality_gate(batch)  # => co-18: run the quality gate -- always runs, right after extract
    print(f"Extracted batch: {batch} | Quality gate passed: {gate_passed}")  # => co-18: prints the batch and the gate's verdict
    if gate_passed:  # => co-18: load is WIRED to depend on the gate -- it only runs if the gate passed
        load(batch)  # => co-18: this line must be UNREACHABLE for this deliberately bad batch
    print(f"Tasks that actually ran: {TASK_LOG}")  # => co-18: prints the complete, final task log

    assert gate_passed is False, "this deliberately bad batch (contains -5) must fail the quality gate"  # => co-18: sanity check
    assert TASK_LOG == ["extract", "quality_gate"], "load must be SKIPPED entirely when the quality gate fails"  # => co-18: the claim ex-44 makes
    print("MATCH: extract and quality_gate ran; load never ran -- the bad batch never reached the load step")  # => co-18
    # => co-18: wiring co-16's checks AS a DAG task is what turns "we should validate data" into "a bad batch cannot physically proceed"
