"""Example 49: Levenshtein Edit Distance -- a 2D DP Table."""

# dp[i][j] = min edits to turn word1[:i] into word2[:j] (co-24): if the last
# characters match, no edit is needed there -- reuse dp[i-1][j-1] directly.
# Otherwise, try all three edits (insert, delete, substitute) and take the
# cheapest, each reducing to a smaller, already-solved subproblem.


def edit_distance(word1: str, word2: str) -> int:  # => O(m*n) time and space
    m, n = len(word1), len(word2)  # => the two words' lengths
    dp: list[list[int]] = [  # => opens the 2D table construction
        [0] * (n + 1)
        for _ in range(m + 1)  # => one fresh row of zeros per prefix of word1
    ]  # => (m+1) x (n+1) table, one extra row/col for the empty-prefix case
    for i in range(m + 1):  # => turning word1[:i] into "" costs i deletions
        dp[i][0] = i  # => base case along the first column
    for j in range(n + 1):  # => turning "" into word2[:j] costs j insertions
        dp[0][j] = j  # => base case along the first row
    for i in range(1, m + 1):  # => fills the table row by row
        for j in range(1, n + 1):  # => and column by column within each row
            if word1[i - 1] == word2[j - 1]:  # => the last characters already match
                dp[i][j] = dp[i - 1][  # => opens the diagonal-cell lookup
                    j - 1  # => the subproblem for both prefixes shortened by one char
                ]  # => no edit needed here -- reuse the diagonal
            else:  # => the last characters differ -- try each of the three edits
                dp[i][j] = 1 + min(
                    dp[i - 1][j],  # => DELETE word1[i-1]
                    dp[i][j - 1],  # => INSERT word2[j-1]
                    dp[i - 1][j - 1],  # => SUBSTITUTE word1[i-1] for word2[j-1]
                )  # => plus 1 for whichever edit was cheapest
    return dp[m][n]  # => the bottom-right cell: the full-word edit distance


print(edit_distance("kitten", "sitting"))  # => Output: 3 -- k->s, e->i, +g
print(edit_distance("", "abc"))  # => Output: 3 -- three insertions
print(edit_distance("same", "same"))  # => Output: 0 -- identical words need no edits

assert (  # => opens the classic-example check
    edit_distance("kitten", "sitting")
    == 3  # => True only if the computed distance is 3
)  # => confirms the classic example's answer
assert edit_distance("", "abc") == 3  # => confirms the empty-string edge case
assert edit_distance("same", "same") == 0  # => confirms identical strings cost nothing
assert edit_distance("abc", "") == 3  # => confirms the mirrored empty-string case
print("ex-49 OK")  # => Output: ex-49 OK
