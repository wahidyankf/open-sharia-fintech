"""Example 67: pytest verification for Imperative-to-Functional Refactor."""

from example import running_max_and_sum_mutation_heavy, running_max_and_sum_pure_fold


def test_both_versions_compute_the_identical_output() -> None:
    mutable = [10, 20, 5]  # => fresh input, isolated from the module-level demo
    before = running_max_and_sum_mutation_heavy(mutable)
    after = running_max_and_sum_pure_fold((10, 20, 5))  # => the same original values as a tuple
    assert before == after  # => same sum and max, regardless of mutation style


def test_pure_fold_never_mutates_its_input() -> None:
    original = (7, 8, 9)  # => fresh immutable input
    running_max_and_sum_pure_fold(original)  # => call once, discard the result
    assert original == (7, 8, 9)  # => provably unchanged -- tuples can't be mutated in place anyway,
    # => but this documents the deliberate contract the refactor was written to satisfy


# => Run: pytest -- Output: 2 passed
