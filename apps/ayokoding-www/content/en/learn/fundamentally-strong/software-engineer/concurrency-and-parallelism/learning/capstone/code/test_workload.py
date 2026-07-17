"""Capstone: pytest verification for workload.py's baseline fetch and aggregate."""

from workload import (
    CPU_UNIT_ITERATIONS,
    PAGE_COUNT,
    PARALLEL_UNITS,
    SERIAL_UNITS,
    run_serial_aggregate,
    run_serial_fetch,
    run_serial_pipeline,
)


def test_serial_fetch_produces_correct_pages() -> None:
    _elapsed, pages = run_serial_fetch()
    assert pages == [n * n for n in range(PAGE_COUNT)]


def test_serial_aggregate_produces_correct_total() -> None:
    _elapsed, total = run_serial_aggregate()
    expected_unit = CPU_UNIT_ITERATIONS * (CPU_UNIT_ITERATIONS - 1) // 2
    assert total == expected_unit * (SERIAL_UNITS + PARALLEL_UNITS)


def test_serial_pipeline_combines_both() -> None:
    elapsed, pages, total = run_serial_pipeline()
    assert pages == [n * n for n in range(PAGE_COUNT)]
    assert total > 0
    assert elapsed > 0


# => Run: pytest -- Output: 3 passed
