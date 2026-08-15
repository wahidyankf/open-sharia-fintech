# A dataclass keeps success fields explicit and stable.
from dataclasses import dataclass


# A result has data instead of unstructured prose.
@dataclass(frozen=True)
class Result:
    # The flag lets callers branch without parsing text.
    ok: bool
    # The computed value is the useful observation.
    value: int
    # The unit removes ambiguity from the value.
    unit: str


# This handler is local and deterministic.
def temperature() -> Result:
    # Return only fields needed for the next decision.
    return Result(True, 30, "C")


# The assertion protects the result contract.
assert temperature() == Result(True, 30, "C")
# The record shows the model-readable shape.
print(temperature())
