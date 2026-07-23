"""Example 52: pytest verification for an `asyncio.Queue` Producer/Consumer Pipeline."""

import asyncio

from example import ITEM_COUNT, run_pipeline


def test_all_items_consumed_cooperatively_in_order() -> None:
    collected = asyncio.run(run_pipeline())
    assert collected == list(range(ITEM_COUNT))  # => every item arrived, in order, none lost


# => Run: pytest -- Output: 1 passed
