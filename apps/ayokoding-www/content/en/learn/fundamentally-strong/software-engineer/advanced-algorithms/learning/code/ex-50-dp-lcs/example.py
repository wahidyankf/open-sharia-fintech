"""Example 50: Longest Common Subsequence -- DP Table, Then Reconstruction."""

# dp[i][j] = LCS length of word1[:i] and word2[:j] (co-24): matching last
# characters extend the diagonal's LCS by one; otherwise, take the better of
# dropping ONE character from either string. RECONSTRUCTION then walks the
# filled table backward, following exactly which choice produced each cell.


def lcs_length_table(  # => builds the full DP table, bottom-up, one cell at a time
    word1: str,  # => the first string being compared
    word2: str,  # => the two strings to compare
) -> list[list[int]]:  # => O(m*n) table build
    m, n = len(word1), len(word2)  # => the two strings' lengths
    dp: list[list[int]] = [  # => opens the 2D table construction
        [0] * (n + 1)  # => one zero-filled row per prefix length of word1
        for _ in range(m + 1)  # => one fresh row of zeros per prefix of word1
    ]  # => dp[i][0] and dp[0][j] are already 0 -- an empty prefix has LCS length 0
    for i in range(1, m + 1):  # => fills row by row
        for j in range(1, n + 1):  # => and column by column
            if word1[i - 1] == word2[j - 1]:  # => the last characters MATCH
                dp[i][j] = dp[i - 1][j - 1] + 1  # => extends the diagonal's LCS by one
            else:  # => no match -- the LCS must drop ONE character from either string
                dp[i][j] = max(
                    dp[i - 1][j],  # => value if word1's last char is dropped
                    dp[i][j - 1],  # => value if word2's last char is dropped
                )  # => takes whichever drop preserves the longer LCS
    return dp  # => the full table -- dp[m][n] is the final LCS length


def reconstruct_lcs(  # => retraces which choice built each cell, to recover the actual chars
    word1: str,  # => the same first string used to build the table
    word2: str,  # => the same second string used to build the table
    dp: list[list[int]],  # => the original strings + filled table
) -> str:  # => walks the table BACKWARD from (m, n)
    i, j = len(word1), len(word2)  # => starts at the bottom-right cell
    chars: list[str] = []  # => accumulates matched characters, in REVERSE order
    while i > 0 and j > 0:  # => stops once either string is exhausted
        if (  # => opens the match check
            word1[i - 1] == word2[j - 1]
        ):  # => this position was a MATCH -- part of the LCS
            chars.append(word1[i - 1])  # => records this matched character
            i -= 1  # => moves diagonally, retracing the match
            j -= 1  # => both indices step back together on a diagonal match
        elif dp[i - 1][j] >= dp[i][j - 1]:  # => the LCS came from dropping word1's char
            i -= 1  # => moves up, following that earlier decision
        else:  # => the LCS came from dropping word2's char instead
            j -= 1  # => moves left, following THAT earlier decision
    return "".join(reversed(chars))  # => reverses back to forward reading order


# demonstrates the full pipeline: build the table, then reconstruct from it
word1, word2 = "ABCBDAB", "BDCABA"  # => the classic LCS example pair
table = lcs_length_table(word1, word2)  # => builds the DP table once
length = table[len(word1)][len(word2)]  # => the LCS length, read from the final cell
sequence = reconstruct_lcs(word1, word2, table)  # => the actual matched subsequence
print(length)  # => Output: 4
print(sequence)  # => Output: BCBA

assert length == 4  # => confirms the known LCS length for this classic example
assert len(sequence) == length  # => confirms the reconstructed string has that length
assert sequence == "BCBA"  # => confirms the exact reconstructed subsequence
print("ex-50 OK")  # => Output: ex-50 OK
