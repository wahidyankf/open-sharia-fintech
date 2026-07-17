"""Example 4: pytest verification for Mutable Variable Box."""

import example


def test_aliased_list_mutation_is_visible_through_the_original_name() -> None:
    original: list[int] = [1, 2, 3]  # => fresh list, isolated from the module-level demo
    alias: list[int] = original  # => alias shares the same underlying object
    alias.append(99)  # => mutate through the alias
    assert original == [1, 2, 3, 99]  # => the mutation is visible through the original name too
    assert original is alias  # => same object identity, not two equal-but-separate lists


def test_module_level_demo_matches_documented_output() -> None:
    assert example.original == [1, 2, 3, 4]  # => the module-level list after its own append
    assert example.alias is example.original  # => same shared-box guarantee at module scope


# => Run: pytest -- Output: 2 passed
