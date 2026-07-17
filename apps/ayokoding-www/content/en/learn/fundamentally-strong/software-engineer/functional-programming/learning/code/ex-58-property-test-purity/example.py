"""Example 58: Property-Testing Purity Without a Third-Party Library."""

import random  # => stdlib source of pseudo-random test inputs -- no third-party library needed


def normalize_score(
    raw: int,
) -> int:  # => the function under test: clamps a raw score into 0..100
    return max(0, min(100, raw))  # => pure: same raw always clamps to the same result


random.seed(
    1234
)  # => a FIXED seed makes this "random" test fully reproducible on every run
generated_inputs = [
    random.randint(-500, 500) for _ in range(200)
]  # => 200 pseudo-random raw scores

first_pass = [
    normalize_score(x) for x in generated_inputs
]  # => calls the function ONCE per input
second_pass = [
    normalize_score(x) for x in generated_inputs
]  # => calls it AGAIN, same inputs, later

purity_property_holds = (
    first_pass == second_pass
)  # => THE property: two independent runs agree exactly

# => property-based testing checks an invariant across MANY generated inputs, not one
print(
    purity_property_holds
)  # => Output: True -- purity verified across all 200 generated inputs, not one
print(
    len(generated_inputs)
)  # => Output: 200 -- a property test checks MANY cases, not a single example
