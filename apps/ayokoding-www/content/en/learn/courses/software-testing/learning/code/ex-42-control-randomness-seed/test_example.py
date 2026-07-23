# learning/code/ex-42-control-randomness-seed/test_example.py
"""Example 42: Seeding Randomness."""

import random  # => stdlib's random module -- normally non-deterministic across runs (co-26)

import pytest  # => brings in @pytest.fixture, used to seed the RNG before each test


@pytest.fixture
def seeded_random():  # => a fixture that SEEDS the shared random module before the test runs (co-26, co-05)  # fmt: skip
    random.seed(42)  # => a FIXED seed -- makes every subsequent random.* call reproducible  # fmt: skip
    yield random  # => hands the (now-seeded) random module itself to the test  # fmt: skip


def test_seeded_random_is_reproducible(seeded_random) -> None:
    first_value = seeded_random.randint(1, 100)  # => act: the FIRST "random" draw after seeding  # fmt: skip
    second_value = seeded_random.randint(1, 100)  # => act: the SECOND draw, same seeded sequence  # fmt: skip
    # => these exact values are DETERMINED entirely by seed 42 -- re-running this test
    # => (or this whole file) produces the IDENTICAL two numbers, every single time
    assert first_value == 82  # => genuinely reproducible: seed(42) always yields 82 first, on CPython 3.13  # fmt: skip
    assert second_value == 15  # => and always 15 second -- verified by actually running this file  # fmt: skip
