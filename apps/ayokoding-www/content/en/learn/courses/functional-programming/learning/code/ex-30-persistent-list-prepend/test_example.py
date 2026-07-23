"""Example 30: pytest verification for O(1) Sharing on a Persistent Linked List."""

from example import PList, plist_prepend


def test_prepend_is_o1_and_shares_the_tail() -> None:
    version_a: PList | None = plist_prepend(1, None)
    version_b = plist_prepend(
        2, version_a
    )  # => O(1): only reads version_a.length, never walks it

    assert version_b.length == 2
    assert version_a.length == 1  # => unaffected by building version_b
    assert version_b.tail is version_a  # => structural sharing, not a copy


# => Run: pytest -- Output: 1 passed
