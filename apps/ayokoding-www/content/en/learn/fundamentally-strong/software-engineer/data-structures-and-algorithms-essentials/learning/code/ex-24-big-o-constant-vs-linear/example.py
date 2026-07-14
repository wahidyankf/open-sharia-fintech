"""Example 24: Big-O in Practice -- O(1) Dict Lookup vs O(n) List Scan."""


# A dict lookup takes exactly 1 "step" regardless of dict size (co-01, co-08).
def dict_lookup_steps(
    lookup: dict[int, int], target: int
) -> int:  # => step-counting version
    _ = lookup.get(target)  # => hashing does the work -- no per-element counting needed
    return 1  # => O(1): the step count never grows with len(lookup)


# A worst-case list scan takes len(items) "steps" -- grows with n (co-01, co-13).
def list_scan_steps(items: list[int], target: int) -> int:  # => step-counting version
    steps = 0  # => counts how many elements get examined
    for value in items:  # => O(n): must potentially look at every element
        steps += 1  # => one step per element visited
        if value == target:  # => stops counting early once found
            break  # => stops early on a match, but the LAST element is worst case
    return steps  # => the number of elements actually examined


for n in (10, 100, 1000):  # => grows the input size across three trials
    lookup = {i: i for i in range(n)}  # => a dict with n entries
    items = list(range(n))  # => a list with n entries, target absent from both
    dict_steps = dict_lookup_steps(lookup, target=-1)  # => -1 is never a key
    list_steps = list_scan_steps(items, target=-1)  # => -1 forces a full scan
    print(f"n={n}: dict_steps={dict_steps}, list_steps={list_steps}")
    # => Output (n=10):   n=10: dict_steps=1, list_steps=10
    # => Output (n=100):  n=100: dict_steps=1, list_steps=100
    # => Output (n=1000): n=1000: dict_steps=1, list_steps=1000
    assert dict_steps == 1  # => confirms the dict step count never grows with n
    assert list_steps == n  # => confirms the list step count scales linearly with n

print("ex-24 OK")  # => Output: ex-24 OK
