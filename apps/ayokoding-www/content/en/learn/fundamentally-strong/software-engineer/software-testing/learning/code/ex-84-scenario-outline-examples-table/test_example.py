"""Example 84: One Scenario Outline, Driven Over an Examples Table -- Each Row, Its Own Case."""
# A Scenario Outline with an Examples table runs its <placeholder>-templated steps once PER ROW --
# pytest-bdd expands three table rows into three separately-reported test cases, Gherkin's own
# version of parametrization (co-06), covering three shipping thresholds without repeating prose.

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python

from pytest_bdd import given, scenario, then, when  # => co-31: pytest-bdd's binding decorators  # fmt: skip
from pytest_bdd.parsers import parse  # => co-31: extracts the TYPED <total>/<tier> placeholders  # fmt: skip


def shipping_tier(total: float) -> str:  # => co-31: the pure logic each Examples row exercises  # fmt: skip
    if total >= 100:  # => co-31: the THIRD row's threshold -- exercised by total=150  # fmt: skip
        return "free"  # => co-31: the highest tier, reached only above the top threshold  # fmt: skip
    if total >= 50:  # => co-31: the SECOND row's threshold -- exercised by total=60  # fmt: skip
        return "discounted"  # => co-31: the middle tier  # fmt: skip
    return "standard"  # => co-31: the FIRST row's fallback -- exercised by total=10  # fmt: skip


@scenario(  # => co-31: pytest-bdd expands the Examples TABLE into one test PER ROW automatically  # fmt: skip
    "features/shipping_tier.feature", "Order total determines the shipping tier"
)
def test_order_total_determines_the_shipping_tier() -> None: ...  # => co-31/co-06: the outline's ONE  # fmt: skip


# => scenario name -- pytest reports it as MULTIPLE test IDs, one per Examples row, below


@given(parse("an order total of {total:d}"), target_fixture="total")  # => co-31: <total> substituted  # fmt: skip
def an_order_total(total: int) -> int:  # => co-06: a DIFFERENT int per row -- 10, then 60, then 150  # fmt: skip
    return total  # => co-31: published as the "total" fixture the WHEN step below requests  # fmt: skip


@when("the shipping tier is computed", target_fixture="tier")  # => co-31: the SAME action, every row  # fmt: skip
def the_shipping_tier_is_computed(total: int) -> str:  # => co-31: requests the GIVEN's "total" fixture  # fmt: skip
    return shipping_tier(
        total
    )  # => co-31: the SAME pure function tested directly at the top of this file


@then(
    parse('the tier is "{expected}"')
)  # => co-31: <tier> substituted -- checked against EACH row's own value
def the_tier_is(tier: str, expected: str) -> None:  # => co-31: requests the WHEN step's "tier" fixture  # fmt: skip
    assert tier == expected  # => co-31: three DIFFERENT expected values, three DIFFERENT real checks  # fmt: skip
