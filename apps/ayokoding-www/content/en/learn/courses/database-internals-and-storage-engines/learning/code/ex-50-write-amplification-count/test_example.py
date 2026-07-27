"""Example 50: pytest verification for Write Amplification Counting."""

import example


def test_write_amplification_exceeds_one() -> None:
    example.application_bytes = 0
    example.disk_bytes_written = 0
    example.flush_memtable({"x": "1"})
    example.compact([{"x": "1"}])
    assert example.disk_bytes_written / example.application_bytes > 1


def test_a_single_flush_with_no_compaction_has_amplification_one() -> None:
    example.application_bytes = 0
    example.disk_bytes_written = 0
    example.flush_memtable({"x": "1"})
    assert example.disk_bytes_written / example.application_bytes == 1


# => Run: pytest -- Output: 2 passed
