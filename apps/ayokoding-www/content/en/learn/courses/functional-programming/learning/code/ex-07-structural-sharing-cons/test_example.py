"""Example 7: pytest verification for A Persistent Cons-List Prepend."""

from example import ConsList, prepend, to_list


def test_prepend_shares_the_old_tail() -> None:
    version_a: ConsList | None = prepend(1, None)  # => [1]
    version_b = prepend(2, version_a)  # => [2, 1], reusing version_a as tail

    assert to_list(version_a) == [1]  # => version_a unaffected by building version_b
    assert to_list(version_b) == [2, 1]
    assert version_b.tail is version_a  # => structural sharing, not a copy


# => Run: pytest -- Output: 1 passed
