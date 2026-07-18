"""Example 12: LSD Radix Sort -- Counting Sort, One Digit at a Time."""

# Radix sort (co-10) sorts fixed-width integers digit by digit, Least
# Significant Digit first, using a STABLE counting-sort pass per digit
# (co-11) -- stability is what lets earlier passes' order survive later ones.


def counting_sort_by_digit(  # => one STABLE counting-sort pass over a single digit
    items: list[int],
    digit_place: int,  # => digit_place selects ones/tens/hundreds/...
) -> list[int]:  # => sorts by ONE digit (0-9) at digit_place, stably
    counts: list[int] = [0] * 10  # => one bucket per digit value, 0 through 9
    for value in items:  # => O(n): tallies each item's digit at this place
        digit = (value // digit_place) % 10  # => extracts just this one digit
        counts[digit] += 1  # => increments that digit's bucket
    for i in range(1, 10):  # => converts counts into a running prefix sum
        counts[i] += counts[i - 1]  # => counts[d] = "how many items have digit <= d"
    result: list[int] = [0] * len(items)  # => pre-allocated stable output
    for value in reversed(items):  # => backward pass preserves relative order (co-11)
        digit = (value // digit_place) % 10  # => this item's digit at digit_place
        counts[digit] -= 1  # => converts the running count to a 0-based index
        result[counts[digit]] = value  # => places value at its position for this pass
    return result  # => stably re-ordered by this one digit


def radix_sort(items: list[int]) -> list[int]:  # => sorts non-negative fixed-width ints
    if not items:  # => the empty-list edge case needs no digit passes at all
        return []  # => nothing to sort
    result = list(items)  # => a working copy -- the original input is never mutated
    max_value = max(result)  # => determines how many digit passes are needed
    digit_place = 1  # => starts at the ONES place (10^0)
    while max_value // digit_place > 0:  # => stops once digit_place exceeds max_value
        result = counting_sort_by_digit(result, digit_place)  # => one stable digit pass
        digit_place *= 10  # => moves to the next digit place (tens, hundreds, ...)
    return result  # => fully sorted after enough digit passes


data: list[int] = [
    170,  # => 3-digit value -- exercises the hundreds-place pass
    45,  # => 2-digit value
    75,  # => 2-digit value, shares tens digit "7" with 75 vs 170's hundreds
    90,  # => 2-digit value, ones digit is 0
    802,  # => the LARGEST value -- fixes the pass count at 3 (max_value // 100 > 0)
    24,  # => 2-digit value
    2,  # => single-digit value -- ones digit only, zero-padded implicitly
    66,  # => 2-digit value with matching tens and ones digits
]  # => mixed 1-3 digit non-negative ints
sorted_data = radix_sort(data)  # => LSD radix sort, three digit passes (max is 802)
print(sorted_data)  # => Output: [2, 24, 45, 66, 75, 90, 170, 802]

assert sorted_data == [  # => opens the expected fully-sorted comparison list
    2,  # => smallest value -- must sort first
    24,  # => 2nd smallest
    45,  # => 3rd smallest
    66,  # => 4th -- both digits happened to match, unaffected by stability quirks
    75,  # => 5th
    90,  # => 6th -- trailing zero digit, still sorts correctly
    170,  # => 7th -- first 3-digit value in the output
    802,  # => largest value -- must sort last
]  # => confirms ascending order
assert sorted_data == sorted(data)  # => matches Python's own sort too
assert radix_sort([]) == []  # => confirms the empty-input edge case
print("ex-12 OK")  # => Output: ex-12 OK
