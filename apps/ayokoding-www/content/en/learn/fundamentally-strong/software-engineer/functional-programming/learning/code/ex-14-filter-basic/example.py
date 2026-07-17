"""Example 14: filter() Keeps Only Evens."""


def is_even(n: int) -> bool:  # => the predicate filter will apply to each element
    return n % 2 == 0  # => True keeps the element, False drops it


nums = [1, 2, 3, 4, 5, 6, 7, 8]  # => the source sequence

evens = filter(
    is_even, nums
)  # => LAZY: builds an iterator, no filtering has happened yet
evens_list = list(evens)  # => forces evaluation -- runs is_even on every element

print(evens_list)  # => Output: [2, 4, 6, 8]
print(len(evens_list))  # => Output: 4 -- exactly half of the original 8 elements
print(
    all(n % 2 == 0 for n in evens_list)
)  # => Output: True -- odds were dropped, not zeroed
