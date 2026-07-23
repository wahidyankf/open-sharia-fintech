"""Example 6: pytest verification for OO Word Count."""

from example import WordCounter


def test_count_via_method_matches_imperative_version() -> None:
    counter = WordCounter()  # => fresh instance, isolated from the module-level demo
    for word in "the cat sat on the mat the cat ran".split():
        counter.add(word)  # => behavior bundled with state -- no external dict
    assert counter.result() == {"the": 3, "cat": 2, "sat": 1, "on": 1, "mat": 1, "ran": 1}


def test_two_instances_have_independent_state() -> None:
    a = WordCounter()  # => instance A
    b = WordCounter()  # => instance B, a separate object entirely
    a.add("x")  # => mutate only A
    assert a.result() == {"x": 1}  # => A reflects the mutation
    assert b.result() == {}  # => B is untouched -- proves state is per-instance, not shared


# => Run: pytest -- Output: 2 passed
