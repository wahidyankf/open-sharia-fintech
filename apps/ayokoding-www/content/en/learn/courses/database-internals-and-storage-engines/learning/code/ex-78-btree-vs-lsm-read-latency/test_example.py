"""Example 78: pytest verification for B-Tree vs LSM Read Latency."""

from example import btree_simulated_page_reads, lsm_simulated_page_reads


def test_btree_read_cost_stays_low_for_a_large_key_count() -> None:
    cost = btree_simulated_page_reads(1_000_000_000, fanout=300)
    assert (
        cost <= 6
    )  # => a shallow tree, even at a billion keys, given a realistic fanout


def test_lsm_read_cost_grows_with_more_uncompacted_segments() -> None:
    fewer = lsm_simulated_page_reads(2)
    more = lsm_simulated_page_reads(20)
    assert more > fewer


# => Run: pytest -- Output: 2 passed
