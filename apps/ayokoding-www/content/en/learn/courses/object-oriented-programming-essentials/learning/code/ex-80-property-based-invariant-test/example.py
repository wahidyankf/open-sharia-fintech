"""Example 80: A Property-Based Test of an Invariant."""

import random  # => imports the random module


class Percentage:  # => begins the Percentage class body
    def __init__(
        self, value: float
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.value = value  # => routes through the validating setter below

    @property  # => marks the next method as a computed attribute
    def value(self) -> float:  # => defines the value() method
        return self._value  # => returns this value to the caller

    @value.setter  # => marks the next method as value's validating setter
    def value(self, v: float) -> None:  # => defines the value() method
        if not (
            0 <= v <= 100
        ):  # => the invariant EVERY constructed instance must satisfy
            raise ValueError(
                "value must be between 0 and 100"
            )  # => rejects out-of-range values
        self._value = v  # => stores _value on this instance


def random_valid_or_invalid(
    rng: random.Random,
) -> float:  # => generates BOTH in- and out-of-range values
    return rng.uniform(
        -50, 150
    )  # => a wide range spanning valid (0-100) and invalid values


rng: random.Random = random.Random(42)  # => a FIXED seed makes this run reproducible
violations: int = 0  # => tallies any successfully constructed, out-of-range Percentage
for _ in range(
    500
):  # => hundreds of randomized inputs, not just a handful of hand-picked ones
    candidate: float = random_valid_or_invalid(rng)  # => constructs candidate
    try:  # => the block below is expected to raise
        p: Percentage = Percentage(candidate)  # => constructs p
        if not (
            0 <= p.value <= 100
        ):  # => if construction ever SUCCEEDS with a bad value, that's a bug
            violations += (
                1  # => would indicate the invariant was violated -- should never happen
            )
    except ValueError:  # => catches the ValueError raised above
        pass  # => the expected outcome for an out-of-range candidate
print(
    violations
)  # => zero means no generated input ever reached an invalid constructed state
# => Output: 0
# => Testing an invariant against hundreds of randomized inputs is a much stronger claim than a couple of hand-picked edge cases
