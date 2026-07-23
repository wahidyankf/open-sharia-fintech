"""Example 9: pytest verification for `x += 1` Is Not One Atomic Step."""

from example import bump, opnames_for


def test_increment_compiles_to_separate_load_and_store() -> None:
    names = opnames_for(bump)
    assert "LOAD_GLOBAL" in names  # => the read
    assert "STORE_GLOBAL" in names  # => the write
    assert names.index("LOAD_GLOBAL") < names.index("STORE_GLOBAL")  # => read strictly precedes write


# => Run: pytest -- Output: 1 passed
