"""Example 25: pytest verification for Template Method: One Skeleton, Many Subclasses."""

from example import InventoryReport, Report, SalesReport


def test_generate_is_never_duplicated_in_either_subclass() -> None:
    # => the mechanical proof: both subclasses inherit the EXACT SAME generate() object
    assert SalesReport.generate is Report.generate  # => no override anywhere
    assert InventoryReport.generate is Report.generate  # => no override here either


def test_each_subclass_still_produces_its_own_body() -> None:
    sales: SalesReport = SalesReport()
    inventory: InventoryReport = InventoryReport()
    assert "Sales: $1000" in sales.generate()
    assert "Stock: 42 units" in inventory.generate()  # => a genuinely different body


# => Run: pytest -- Output: 2 passed
