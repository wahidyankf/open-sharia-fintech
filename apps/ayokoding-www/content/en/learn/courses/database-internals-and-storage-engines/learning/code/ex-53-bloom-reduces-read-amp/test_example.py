"""Example 53: pytest verification for Bloom Filters Reducing Read Amplification."""

from example import SSTable, point_read


def test_absent_key_opens_fewer_tables_than_exist() -> None:
    tables = [SSTable() for _ in range(4)]
    for i, table in enumerate(tables):
        table.add(f"present-{i}", "v")
    _, opened = point_read("definitely-absent", tables)
    assert opened < len(tables)


def test_present_key_is_still_found_correctly() -> None:
    table = SSTable()
    table.add("k", "v")
    value, _ = point_read("k", [table])
    assert value == "v"


# => Run: pytest -- Output: 2 passed
