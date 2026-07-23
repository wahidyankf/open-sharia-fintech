"""Example 50: pytest verification for Paradigm Soup Anti-Pattern."""

from example import MutableBucket, add_bonus_functional_looking, scale_functional_looking


def test_aliasing_bug_reproduces_original_is_silently_mutated() -> None:
    original = MutableBucket([1, 2, 3])  # => fresh bucket, isolated from the module-level demo
    result = scale_functional_looking(add_bonus_functional_looking(original))  # => a "functional-looking" chain

    assert result.items == [2, 4, 6, 1998]  # => the chained result
    assert original.items == [2, 4, 6, 1998]  # => THE BUG: the "original" reference was mutated too
    assert original is result  # => same object identity -- no new value was ever produced


def test_a_true_immutable_pipeline_would_not_have_this_bug() -> None:
    original: tuple[int, ...] = (1, 2, 3)  # => the honest functional fix: use an immutable tuple instead
    bonus = original + (999,)  # => a genuinely NEW tuple, original untouched
    scaled = tuple(n * 2 for n in bonus)  # => another genuinely NEW tuple
    assert original == (1, 2, 3)  # => the true-functional version never mutates the original at all
    assert scaled == (2, 4, 6, 1998)  # => and still produces the identical final values


# => Run: pytest -- Output: 2 passed
