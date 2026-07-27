"""Worked Example 41: DAG Task Dependencies -- Topological Order."""  # => co-18: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

DEPENDENCIES = {  # => co-18: task -> the set of tasks it depends on -- Airflow's own "wires tasks with dependencies" shape
    "extract": set(),  # => co-18: extract has no upstream dependency -- it can run first
    "transform": {"extract"},  # => co-18: transform depends on extract having already run
    "load": {"transform"},  # => co-18: load depends on transform having already run
}  # => co-18: closes DEPENDENCIES -- a simple three-task, linear DAG: extract -> transform -> load


def topological_order(dependencies: dict[str, set[str]]) -> list[str]:  # => co-18: the scheduler's own core algorithm, simplified
    """Return tasks in an order where every task appears only after all of its dependencies."""  # => co-18: documents topological_order's contract -- no runtime output, just sets its __doc__
    completed: list[str] = []  # => co-18: tasks that have already "run," in the order they ran
    remaining = dict(dependencies)  # => co-18: a working copy -- shrinks as tasks complete
    while remaining:  # => co-18: keep scheduling until every task has run
        ready = [task for task, deps in remaining.items() if deps.issubset(completed)]  # => co-18: a task is READY once every dependency has completed
        if not ready:  # => co-18: nothing is ready -- would indicate a cycle, which this fixture deliberately does not have
            raise RuntimeError("cycle detected -- no task is ready to run")  # => co-18: fails loudly rather than looping forever
        for task in sorted(ready):  # => co-18: sorted for a DETERMINISTIC, reproducible transcript across runs
            completed.append(task)  # => co-18: mark this task as having "run"
            del remaining[task]  # => co-18: remove it from the working set
    return completed  # => co-18: returns this computed value to the caller


if __name__ == "__main__":  # => co-18: entry point -- runs only when this file executes directly, not on import
    run_order = topological_order(DEPENDENCIES)  # => co-18: compute the scheduler's actual run order
    print(f"Tasks run in order: {run_order}")  # => co-18: prints the exact order the scheduler chose

    extract_before_transform = run_order.index("extract") < run_order.index("transform")  # => co-18: dependency order check 1
    transform_before_load = run_order.index("transform") < run_order.index("load")  # => co-18: dependency order check 2
    print(f"extract before transform: {extract_before_transform} | transform before load: {transform_before_load}")  # => co-18
    assert extract_before_transform and transform_before_load, "every task must run only after all its dependencies have run"  # => co-18
    print(f"MATCH: {run_order} respects every declared dependency edge in the DAG")  # => co-18
    # => co-18: the scheduler's whole job is exactly this -- run a task once, and only once, its dependencies are satisfied
