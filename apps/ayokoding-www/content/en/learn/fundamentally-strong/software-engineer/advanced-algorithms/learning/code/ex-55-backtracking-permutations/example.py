"""Example 55: Enumerate All Permutations by Backtracking -- Exactly n! of Them."""

# At each position, backtracking (co-25) tries every UNUSED item; n choices
# for the first slot, n-1 for the second, and so on -- the classic n!
# counting argument, realized directly as recursive choice-and-undo.


def all_permutations(  # => builds every ordering by choosing one UNUSED item at a time
    items: list[int],  # => the items to permute
) -> list[list[int]]:  # => returns all n! orderings
    result: list[list[int]] = []  # => accumulates every complete permutation
    current: list[int] = []  # => the in-progress permutation being built
    used: set[int] = set()  # => which items are already placed in `current`

    def backtrack() -> (
        None
    ):  # => fills the next position, then backtracks to try others
        if len(current) == len(items):  # => base case: every item has been placed
            result.append(list(current))  # => records a COPY of the completed ordering
            return
        for item in items:  # => tries every item as the NEXT position's value
            if item in used:  # => already placed earlier in this branch -- skip it
                continue  # => THE PRUNE: never reconsider an already-used item
            used.add(item)  # => marks item as placed
            current.append(item)  # => appends it to the in-progress ordering
            backtrack()  # => recurses to fill the remaining positions
            current.pop()  # => BACKTRACK: undoes the append
            used.remove(item)  # => frees item for other branches

    backtrack()  # => starts with an empty ordering
    return result  # => every one of the n! possible orderings


items: list[int] = [1, 2, 3]  # => a small 3-element set
perms = all_permutations(items)  # => all 6 permutations of [1, 2, 3]
print(len(perms))  # => Output: 6
print(  # => opens the sorted-permutations print call
    sorted(perms)  # => sorts for a deterministic, readable print order
)  # => Output: [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]

assert len(perms) == 6  # => 3! = 6, confirms the exact expected count
unique_perms = {tuple(p) for p in perms}  # => tuples are hashable, catching duplicates
assert len(unique_perms) == len(perms)  # => confirms every permutation is DISTINCT
for p in perms:  # => confirms every permutation is a valid rearrangement of items
    assert sorted(p) == sorted(items)  # => same multiset of elements, just reordered
print("ex-55 OK")  # => Output: ex-55 OK
