"""Example 54: Enumerate All Subsets by Backtracking -- Exactly 2^n of Them."""

# At each element, backtracking (co-25) branches into TWO choices: include
# it, or don't. n independent binary choices produce exactly 2^n leaves --
# no pruning needed here, since every combination of choices is valid.


def all_subsets(items: list[int]) -> list[list[int]]:  # => returns all 2^n subsets
    result: list[list[int]] = []  # => accumulates every complete subset found
    current: list[int] = []  # => the in-progress subset being built

    def backtrack(index: int) -> None:  # => decides item[index]'s fate: in or out
        if index == len(items):  # => base case: every item has been decided
            result.append(list(current))  # => records a COPY -- current keeps mutating
            return
        current.append(items[index])  # => CHOICE 1: include this item
        backtrack(index + 1)  # => explores every subset that includes it
        current.pop()  # => BACKTRACK: undoes that inclusion
        backtrack(index + 1)  # => CHOICE 2: explores every subset that excludes it

    backtrack(0)  # => starts deciding from the first item
    return result  # => every one of the 2^n possible subsets


items: list[int] = [1, 2, 3]  # => a small 3-element set
subsets = all_subsets(items)  # => all 8 subsets of {1, 2, 3}
print(len(subsets))  # => Output: 8
print(  # => opens the sorted-subsets print call
    sorted(subsets)  # => sorts for a deterministic, readable print order
)  # => Output: [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]

assert len(subsets) == 2 ** len(items)  # => confirms exactly 2^n subsets were generated
unique_subsets = {  # => opens the duplicate-detection set comprehension
    tuple(s)
    for s in subsets  # => converts each list subset to a hashable tuple
}  # => tuples are hashable, so a set catches duplicates
assert len(unique_subsets) == len(subsets)  # => confirms NO subset was generated twice
assert [] in subsets  # => confirms the empty subset is included
assert items in subsets  # => confirms the full set itself is included
print("ex-54 OK")  # => Output: ex-54 OK
