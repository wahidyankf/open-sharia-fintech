"""Example 75: pytest verification for The Template Method Pattern."""

from example import SalesReport


def test_fixed_flow_with_only_the_required_hook_overridden() -> None:
    assert (
        SalesReport().build() == "REPORT | sales figures | END"
    )  # => header/footer defaults used


# => Run: pytest -- Output: 1 passed
