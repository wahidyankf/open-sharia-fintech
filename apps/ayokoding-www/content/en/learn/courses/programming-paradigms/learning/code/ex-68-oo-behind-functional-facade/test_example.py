"""Example 68: pytest verification for OO Behind a Functional Facade."""

from example import memoized_lookup


def test_facade_behaves_like_a_pure_lookup_from_the_outside() -> None:
    result_a = memoized_lookup("distinct-key-1", 42)  # => first call for this key
    result_b = memoized_lookup("distinct-key-1", 9999)  # => same key, different compute value
    assert result_a == result_b == 42  # => the cached value wins -- facade has memory, but the API is a function


def test_facade_exposes_no_mutable_state_in_its_own_namespace() -> None:
    public_attrs = [a for a in dir(memoized_lookup) if not a.startswith("__")]  # => introspect the function object
    assert public_attrs == []  # => a plain function has no attributes of its own -- the OO cache stays hidden


# => Run: pytest -- Output: 2 passed
