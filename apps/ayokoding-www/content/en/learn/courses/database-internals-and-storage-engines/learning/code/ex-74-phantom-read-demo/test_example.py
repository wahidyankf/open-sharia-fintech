"""Example 74: pytest verification for the Phantom-Read Anomaly."""

import example
from example import Row


def test_a_concurrently_inserted_row_appears_on_the_second_scan() -> None:
    example.table = [Row(id=1, status="active")]
    first = {row.id for row in example.range_query("active")}
    example.table.append(Row(id=2, status="active"))
    second = {row.id for row in example.range_query("active")}
    assert second - first == {2}


def test_a_row_not_matching_the_predicate_never_becomes_a_phantom() -> None:
    example.table = [Row(id=1, status="active")]
    example.table.append(Row(id=2, status="inactive"))
    result = {row.id for row in example.range_query("active")}
    assert result == {1}


# => Run: pytest -- Output: 2 passed
