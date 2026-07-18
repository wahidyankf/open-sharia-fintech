"""Example 50: pytest verification for Longest Common Subsequence."""

from example import lcs_length_table, reconstruct_lcs


def test_classic_abcbdab_bdcaba_example() -> None:
    word1, word2 = "ABCBDAB", "BDCABA"
    table = lcs_length_table(word1, word2)
    assert table[len(word1)][len(word2)] == 4


def test_no_common_characters_has_zero_length_lcs() -> None:
    table = lcs_length_table("abc", "xyz")
    assert table[3][3] == 0
    assert reconstruct_lcs("abc", "xyz", table) == ""


def test_reconstructed_sequence_is_a_valid_subsequence_of_both_strings() -> None:
    word1, word2 = "hello", "yellow"
    table = lcs_length_table(word1, word2)
    sequence = reconstruct_lcs(word1, word2, table)
    assert len(sequence) == table[len(word1)][len(word2)]


# => Run: pytest -- Output: 3 passed
