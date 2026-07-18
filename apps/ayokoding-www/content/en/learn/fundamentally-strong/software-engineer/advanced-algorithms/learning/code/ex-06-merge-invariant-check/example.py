"""Example 6: Assert the Merge Invariant -- Output Stays Sorted at Every Step."""

# The merge step's INVARIANT (co-07) is: after each append, result is still
# sorted. This example checks that invariant INLINE, after every single
# append, instead of only checking the final list once at the end.


def merge_with_invariant_check(  # => opens the signature -- wraps for line length
    left: list[int],
    right: list[int],  # => both inputs must already be sorted
) -> list[int]:  # => merges two sorted lists, asserting sortedness after each step
    result: list[int] = []  # => the merged output, built one element at a time
    i = j = 0  # => cursors into left and right respectively
    while i < len(left) and j < len(right):  # => while both lists still have elements
        if left[i] <= right[j]:  # => stable tie-break: left wins on equal keys
            result.append(left[i])  # => appends the smaller-or-equal candidate
            i += 1  # => advances the left cursor only
        else:
            result.append(right[j])  # => appends right's strictly smaller candidate
            j += 1  # => advances the right cursor only
        if len(result) >= 2:  # => the invariant only applies once there are 2+ elements
            assert (  # => opens the parenthesized check -- runs after EVERY append
                result[-2] <= result[-1]  # => compares the two most-recent entries
            )  # => THE INVARIANT: the last two appended stay in order
    result.extend(left[i:])  # => appends any leftover left elements (already sorted)
    result.extend(right[j:])  # => appends any leftover right elements (already sorted)
    for k in range(1, len(result)):  # => a final full pass re-checks the WHOLE list
        assert result[k - 1] <= result[k]  # => confirms sortedness end to end
    return result  # => the fully merged, invariant-checked list


left_half: list[int] = [1, 4, 7, 10]  # => a sorted left half
right_half: list[int] = [2, 3, 8, 9]  # => a sorted right half
merged = merge_with_invariant_check(left_half, right_half)  # => merges both halves
print(merged)  # => Output: [1, 2, 3, 4, 7, 8, 9, 10]

assert merged == [1, 2, 3, 4, 7, 8, 9, 10]  # => confirms the final merged order
print("ex-06 OK")  # => Output: ex-06 OK
