"""Example 11: Functional Word Count."""

from collections import Counter  # => a value-producing tool, not a mutation-in-place API
from functools import reduce  # => the classic fold: combine a sequence into one value


def tally_via_counter(words: list[str]) -> Counter[str]:  # => builds a NEW value, doesn't mutate `words`
    return Counter(words)  # => one expression -- Counter never modifies its input list


def tally_via_reduce(words: list[str]) -> dict[str, int]:  # => a fold: no loop body visibly mutates state
    def bump(acc: dict[str, int], word: str) -> dict[str, int]:  # => the fold's combining step
        return {**acc, word: acc.get(word, 0) + 1}  # => returns a BRAND NEW dict every call, no mutation
        # => {**acc, ...} copies acc rather than doing acc[word] += 1 in place

    return reduce(bump, words, {})  # => reduce threads a fresh dict through every step, none shared


words: list[str] = str("the cat sat on the mat the cat ran").split()  # => str(...) widens away the literal so split() returns list[str]
before = tuple(words)  # => snapshot of the input, to prove neither function mutates it
counter_result = tally_via_counter(words)  # => value-producing call
reduce_result = tally_via_reduce(words)  # => value-producing call

print(counter_result["the"], reduce_result["the"])  # => both agree with the imperative version's count
# => Output: 3 3
print(words == list(before))  # => the input list is unchanged -- neither function had a visible mutation
# => Output: True
