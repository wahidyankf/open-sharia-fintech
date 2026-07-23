"""Example 25: __post_init__ Validation."""

from dataclasses import dataclass  # => imports dataclass from dataclasses

ABSOLUTE_ZERO_CELSIUS: float = (
    -273.15
)  # => the physical lower bound this class enforces


@dataclass  # => generates boilerplate methods from the field list below
class Temperature:  # => begins the Temperature class body
    celsius: float  # => a required dataclass field, part of the generated __init__

    def __post_init__(
        self,
    ) -> None:  # => runs automatically right after the generated __init__
        if self.celsius < ABSOLUTE_ZERO_CELSIUS:  # => guards the physical invariant
            raise ValueError(
                "temperature below absolute zero"
            )  # => rejects construction entirely


valid: Temperature = Temperature(
    20.0
)  # => passes validation -- ordinary room temperature
print(valid.celsius)  # => confirms the value survived __post_init__ unchanged
# => Output: 20.0
# => `__post_init__` is where a dataclass validates invariants the generated `__init__` cannot express on its own
