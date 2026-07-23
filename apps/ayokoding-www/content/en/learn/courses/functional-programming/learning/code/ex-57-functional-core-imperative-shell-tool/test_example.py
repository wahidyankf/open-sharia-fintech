"""Example 57: pytest verification for A CSV Analyzer Split into a Pure Core and an I/O Shell."""

from example import format_report, parse_sales, total_by_product


def test_pure_core_needs_no_file_and_no_mocking() -> None:
    csv_text = "product,amount\nx,1.0\nx,2.0\n"
    sales = parse_sales(csv_text)
    totals = total_by_product(sales)
    assert totals == {"x": 3.0}
    assert format_report(totals) == "x: 3.00"


# => Run: pytest -- Output: 1 passed
