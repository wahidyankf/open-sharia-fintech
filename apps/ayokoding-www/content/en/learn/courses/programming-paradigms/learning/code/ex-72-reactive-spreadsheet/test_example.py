"""Example 72: pytest verification for Reactive Spreadsheet."""

from example import Spreadsheet


def test_multi_level_cascade_updates_every_downstream_formula() -> None:
    sheet = Spreadsheet()  # => fresh sheet, isolated from the module-level demo
    sheet.set_value("a1", 1)
    sheet.set_formula("b1", lambda s: s.get("a1") * 10, depends_on=["a1"])
    sheet.set_formula("c1", lambda s: s.get("b1") + 5, depends_on=["b1"])
    assert sheet.get("c1") == 15  # => 1*10+5 at construction time

    sheet.set_value("a1", 2)  # => change the root -- both b1 and c1 must cascade
    assert sheet.get("b1") == 20  # => 2*10
    assert sheet.get("c1") == 25  # => 20+5, reflecting the two-level cascade


def test_unrelated_formula_is_not_affected_by_a_different_cells_update() -> None:
    sheet = Spreadsheet()  # => fresh sheet
    sheet.set_value("x1", 1)
    sheet.set_value("y1", 100)
    sheet.set_formula("z1", lambda s: s.get("x1") + 1, depends_on=["x1"])  # => z1 depends only on x1
    sheet.set_value("y1", 999)  # => update a cell z1 does NOT depend on
    assert sheet.get("z1") == 2  # => z1 is unaffected -- still 1+1


# => Run: pytest -- Output: 2 passed
