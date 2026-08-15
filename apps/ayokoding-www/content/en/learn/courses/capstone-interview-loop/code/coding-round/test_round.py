from round import longest_unique_run, pair_indices


def test_pair_indices_finds_a_complement_and_handles_duplicates() -> None:
    assert pair_indices([2, 7, 11, 15], 9) == (0, 1)
    assert pair_indices([3, 3], 6) == (0, 1)
    assert pair_indices([1, 2], 9) is None


def test_longest_unique_run_moves_the_window_after_a_repeat() -> None:
    assert longest_unique_run("abcabcbb") == 3
    assert longest_unique_run("bbbbb") == 1
    assert longest_unique_run("") == 0
