"""Example 76: Use Fixture Teardown to Reset State Between Tests -- Verify Order-Independence."""
# All three tests pass in BOTH natural and reversed order -- proof that a fresh basket() per
# test, with real teardown, removes any hidden dependency on which test ran before it.

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python

from collections.abc import Iterator  # => types the yield-based fixture's return below  # fmt: skip

import pytest  # => co-05: provides the @pytest.fixture decorator this example builds on  # fmt: skip


class Basket:  # => a small stateful resource -- the kind of thing that WOULD leak across tests  # fmt: skip
    """A mutable basket of item names -- fresh per test, thanks to the fixture below."""  # => co-26

    def __init__(self) -> None:  # => starts with no items -- the fixture's SETUP relies on this  # fmt: skip
        self.items: list[str] = []  # => an empty list, per fresh instance  # fmt: skip

    def add(self, name: str) -> None:  # => the ONE mutation this class exposes  # fmt: skip
        self.items.append(name)  # => appends one item name  # fmt: skip


@pytest.fixture
def basket() -> Iterator[Basket]:  # => co-05: a BRAND NEW Basket per test -- never reused  # fmt: skip
    fresh = Basket()  # => co-05: SETUP -- built fresh, every single time this fixture is requested  # fmt: skip
    yield fresh  # => hands the fresh basket to the test body  # fmt: skip
    fresh.items.clear()  # => co-05/co-26: TEARDOWN -- explicitly empties it, belt-and-braces  # fmt: skip


def test_basket_starts_empty(basket: Basket) -> None:  # => co-26: order-INDEPENDENT by construction  # fmt: skip
    assert basket.items == []  # => true NO MATTER which test ran before this one  # fmt: skip
    basket.add("apple")  # => act: mutates THIS test's own basket only  # fmt: skip


def test_basket_add_one_item(basket: Basket) -> None:  # => co-26: ALSO starts from a clean basket  # fmt: skip
    assert (
        basket.items == []
    )  # => still true, even though the PREVIOUS test added "apple" to ITS OWN basket
    basket.add("bread")  # => act: adds ONE item to a FRESH basket  # fmt: skip
    assert basket.items == ["bread"]  # => only this test's OWN addition is ever visible  # fmt: skip


def test_basket_add_two_items(basket: Basket) -> None:  # => co-26: a THIRD, equally clean basket  # fmt: skip
    assert basket.items == []  # => true again, independent of the two tests above  # fmt: skip
    basket.add("milk")  # => act: first item  # fmt: skip
    basket.add("eggs")  # => act: second item  # fmt: skip
    assert basket.items == ["milk", "eggs"]  # => confirms BOTH additions, in order, on a FRESH basket  # fmt: skip
