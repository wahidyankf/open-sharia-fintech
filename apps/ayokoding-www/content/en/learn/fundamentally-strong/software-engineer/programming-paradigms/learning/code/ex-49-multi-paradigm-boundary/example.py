"""Example 49: Multi-Paradigm Boundary."""

from dataclasses import dataclass


def functional_pipeline(raw_prices: tuple[int, ...]) -> tuple[int, ...]:  # => a pure functional pipeline
    discounted = tuple(p - (p * 10 // 100) for p in raw_prices)  # => map: apply a 10% discount
    return tuple(p for p in discounted if p > 0)  # => filter: drop non-positive prices
    # => every step returns a NEW immutable tuple -- nothing here is ever mutated in place


@dataclass  # => an OO service the pipeline hands its result to, across a clean boundary
class InventoryService:
    accepted_prices: list[int]

    def record_batch(self, prices: tuple[int, ...]) -> None:  # => the ONLY place mutation happens
        self.accepted_prices.extend(prices)  # => OO-style in-place mutation, but confined to this class


raw_prices = (100, 50, 5, 200)  # => an immutable tuple -- the functional side's input
cleaned = functional_pipeline(raw_prices)  # => pure functional processing, no mutation anywhere yet
print(cleaned)  # => 100->90, 50->45, 5->5 (5*10//100=0 discount, still positive), 200->180; nothing dropped
# => Output: (90, 45, 5, 180)

service = InventoryService(accepted_prices=[])  # => the OO side of the boundary
service.record_batch(cleaned)  # => the boundary: an immutable tuple crosses into a mutable OO object
print(service.accepted_prices)  # => confirms the OO side received exactly the functional side's output
# => Output: [90, 45, 5, 180]
print(cleaned)  # => the tuple itself is STILL untouched -- crossing the boundary never mutated it
# => Output: (90, 45, 5, 180)
