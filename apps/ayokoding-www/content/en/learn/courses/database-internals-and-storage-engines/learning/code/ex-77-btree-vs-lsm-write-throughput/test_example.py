"""Example 77: pytest verification for B-Tree vs LSM Write Throughput."""

from example import btree_simulated_page_writes, lsm_simulated_page_writes


def test_lsm_incurs_fewer_simulated_page_writes_for_the_same_insert_count() -> None:
    btree_cost = btree_simulated_page_writes(500)
    lsm_cost = lsm_simulated_page_writes(500, flush_every=50)
    assert lsm_cost < btree_cost


def test_a_larger_flush_batch_further_reduces_lsm_page_writes() -> None:
    small_batch = lsm_simulated_page_writes(1000, flush_every=10)
    large_batch = lsm_simulated_page_writes(1000, flush_every=100)
    assert large_batch < small_batch


# => Run: pytest -- Output: 2 passed
