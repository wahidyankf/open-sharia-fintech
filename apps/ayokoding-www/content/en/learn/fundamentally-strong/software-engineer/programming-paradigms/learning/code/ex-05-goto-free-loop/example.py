"""Example 5: Goto-Free Loop."""


def first_over_ten_hacky(numbers: list[int]) -> int | None:  # => BEFORE: while True + break hack
    i = 0  # => manual index bookkeeping, easy to get wrong
    result: int | None = None  # => mutable box for "have we found it yet"
    while True:  # => an unbounded loop standing in for a goto-style jump target
        if i >= len(numbers):  # => manual bounds check that a for-loop would give for free
            break  # => "jump out" -- the goto-flavored escape hatch
        if numbers[i] > 10:  # => the actual condition we care about
            result = numbers[i]  # => record it
            break  # => a second "jump out" path -- two different reasons to exit the same loop
        i += 1  # => manual index increment, another goto-adjacent footgun
    return result  # => two break statements later, here is the answer


def first_over_ten_clean(numbers: list[int]) -> int | None:  # => AFTER: a plain for + early return
    for n in numbers:  # => a `for` owns its own iteration and bounds -- no manual index
        if n > 10:  # => same condition
            return n  # => a single, obvious exit: return IS the "found it" signal
    return None  # => the natural "ran out without finding it" ending, no flag needed


sample: list[int] = [3, 7, 2, 15, 9, 20]  # => 15 is the first value over 10
print(first_over_ten_hacky(sample))  # => the while-True version's answer
# => Output: 15
print(first_over_ten_clean(sample))  # => the for-loop version's answer -- must match
# => Output: 15
