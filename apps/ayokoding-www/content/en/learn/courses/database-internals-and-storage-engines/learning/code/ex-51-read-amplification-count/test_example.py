"""Example 51: pytest verification for Read Amplification Counting."""

from example import SSTable, point_read


def test_read_amplification_grows_with_segment_count() -> None:
    one_table = [SSTable(data={"z": "1"})]
    four_tables = [SSTable(data={"z": "1"}) for _ in range(4)]
    _, touched_one = point_read(
        "y", one_table
    )  # => "y" is absent -- every table must be checked
    _, touched_four = point_read(
        "y", four_tables
    )  # => same absent key, but four segments to check now
    assert touched_four > touched_one


def test_a_hit_stops_scanning_further_tables() -> None:
    tables = [SSTable(data={"a": "1"}), SSTable(data={"a": "2"})]
    value, touched = point_read("a", tables)
    assert value == "2"
    assert (
        touched == 1
    )  # => the newest table already had the key -- no need to check the older one


# => Run: pytest -- Output: 2 passed
