"""Example 24: chain and groupby Over Data."""

from itertools import (
    chain,
    groupby,
)  # => chain: concatenate iterables; groupby: group consecutive keys

morning = ["apple", "apricot", "banana"]  # => two separately-sourced lists to combine
evening = [
    "blueberry",
    "cherry",
    "avocado",
]  # => notice: NOT globally sorted by first letter

combined = list(
    chain(morning, evening)
)  # => one flat sequence, morning's items THEN evening's
print(combined)  # => shows the raw, unsorted concatenation before grouping
# => Output: ['apple', 'apricot', 'banana', 'blueberry', 'cherry', 'avocado']

grouped = {  # => groupby only groups CONSECUTIVE equal keys -- input must be pre-sorted by key
    letter: list(items)  # => materialize each lazy group before it is invalidated
    for letter, items in groupby(  # => sorted() first, so equal first-letters become consecutive
        sorted(combined),
        key=lambda w: w[0],  # => the grouping key: each word's first letter
    )  # => groupby itself is lazy -- list(items) above is what forces each group
}  # => a plain dict, one entry per distinct first letter seen
print(grouped["a"])  # => Output: ['apple', 'apricot', 'avocado']
print(grouped["b"])  # => Output: ['banana', 'blueberry']
