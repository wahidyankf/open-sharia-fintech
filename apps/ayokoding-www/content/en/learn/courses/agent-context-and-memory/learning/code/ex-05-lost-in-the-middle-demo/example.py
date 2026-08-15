from typing import Final  # => typed recall fixture

SCORES: Final[dict[str, int]] = {
    "early": 3,
    "middle": 1,
    "late": 3,
}  # => fake recall outcome
assert SCORES["middle"] < SCORES["early"]
print("PASS: lost-in-the-middle-demo")  # => weakest slot
