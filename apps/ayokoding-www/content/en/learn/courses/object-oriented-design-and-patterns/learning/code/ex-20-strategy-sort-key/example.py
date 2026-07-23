"""Example 20: Strategy: A Pluggable Sort Key."""  # => module docstring

from dataclasses import dataclass  # => imports dataclass from dataclasses
from typing import Any, Callable  # => Any lets key_func return any sortable type


@dataclass  # => generates __init__ from the fields below
class Item:  # => a simple product record, sortable by more than one field
    name: str  # => the item name, part of the generated __init__
    price: float  # => the item price, part of the generated __init__


def by_name(item: Item) -> str:  # => STRATEGY one: sort key based on name
    return item.name  # => a real, honest sort-key implementation
    # => each strategy is a plain function -- no shared base class required


def by_price(item: Item) -> float:  # => STRATEGY two: sort key based on price
    return item.price  # => a real, honest sort-key implementation


def sort_items(  # => the STRATEGY-ACCEPTING function, spread across lines
    items: list[Item],  # => the data being sorted, unrelated to which strategy is chosen
    key_func: Callable[[Item], Any],
    # => Any (not object) so Pyright accepts str, float, or int keys -- sorted() needs
    # => a genuinely comparable return type, which plain object cannot guarantee
    # => sort_items() is NEVER edited to add a new sorting strategy
) -> list[Item]:  # => defines the sort_items() function
    return sorted(items, key=key_func)  # => delegates the comparison entirely to key_func
    # => any zero-argument-returning callable works as key_func -- functions ARE strategies


items: list[Item] = [
    Item("banana", 1.5),  # => sample item one
    Item("apple", 3.0),  # => sample item two
    Item("cherry", 2.0),  # => sample item three
    # => three sample items, unsorted -- same list, three interchangeable strategies below
]  # => three sample items, unsorted

by_name_result: list[str] = [
    item.name  # => extracts just the name for the printed result
    for item in sort_items(items, by_name)
    # => passes by_name as the STRATEGY object -- a plain function works fine here
]  # => sorted alphabetically via the by_name strategy
by_price_result: list[str] = [
    item.name  # => extracts just the name for the printed result
    for item in sort_items(items, by_price)
    # => passes a DIFFERENT strategy; sort_items() itself did not change at all
]  # => sorted by price via the DIFFERENT by_price strategy, zero edits to sort_items


def by_name_length(item: Item) -> int:  # => a THIRD strategy, added just by writing a function
    return len(item.name)  # => a real, honest sort-key implementation
    # => no class hierarchy needed -- a plain function satisfies the same shape


by_length_result: list[str] = [
    item.name  # => extracts just the name for the printed result
    for item in sort_items(items, by_name_length)
    # => a fourth strategy could be plugged in here the same way, forever
]  # => added with zero changes to sort_items() itself

print(by_name_result, by_price_result, by_length_result)  # => three different orderings
# => three interchangeable strategies, one unmodified sort_items() function
# => Output: ['apple', 'banana', 'cherry'] ['banana', 'cherry', 'apple'] ['apple', 'banana', 'cherry']
# => `sort_items()` was written ONCE and never touched again when `by_name_length` was added
