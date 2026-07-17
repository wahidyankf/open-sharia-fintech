"""Example 20: pytest verification for Strategy: A Pluggable Sort Key."""

from example import Item, by_name, by_price, sort_items


def test_by_name_and_by_price_produce_different_orderings() -> None:
    items: list[Item] = [Item("banana", 1.5), Item("apple", 3.0), Item("cherry", 2.0)]
    by_name_names: list[str] = [item.name for item in sort_items(items, by_name)]
    by_price_names: list[str] = [item.name for item in sort_items(items, by_price)]
    assert by_name_names == ["apple", "banana", "cherry"]
    assert by_price_names == ["banana", "cherry", "apple"]  # => a genuinely different order


def test_a_new_strategy_needs_no_change_to_sort_items() -> None:
    # => defines a fourth strategy right here, inside the test, with zero edits above
    def by_reverse_name(item: Item) -> str:
        return item.name[::-1]

    items: list[Item] = [Item("banana", 1.5), Item("apple", 3.0)]
    result: list[str] = [item.name for item in sort_items(items, by_reverse_name)]
    assert result == ["banana", "apple"]  # => "ananab" sorts before "elppa" reversed


# => Run: pytest -- Output: 2 passed
