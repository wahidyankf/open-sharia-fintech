"""Example 79: pytest verification for Immutable vs Mutable Performance."""

from example import build_via_mutation, build_via_persistent_updates


def test_both_approaches_produce_the_identical_values() -> None:
    n = 500  # => a smaller n than the module-level demo -- correctness, not timing, is what this test checks
    mutated = build_via_mutation(n)
    persistent = build_via_persistent_updates(n)
    assert list(mutated) == list(persistent) == list(range(n))  # => both build the same sequence, correctly


def test_repeated_tuple_concatenation_is_measurably_slower_at_scale() -> None:
    import time

    n = 8000  # => large enough that the O(k) tuple-copy cost dominates measurement noise
    start = time.perf_counter()
    build_via_mutation(n)
    mutation_seconds = time.perf_counter() - start

    start = time.perf_counter()
    build_via_persistent_updates(n)
    persistent_seconds = time.perf_counter() - start

    assert mutation_seconds < persistent_seconds  # => the trade-off this example demonstrates, measured directly


# => Run: pytest -- Output: 2 passed
