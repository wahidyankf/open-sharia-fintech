"""Example 75: Tunable Consistency Latency Tradeoff, Measured."""  # => co-07: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import time  # => co-07: models each simulated replica ack as a real, measurable sleep -- genuine wall-clock latency, not a guess


def simulate_replica_ack_latency_seconds(replica_index: int) -> float:  # => co-07: each replica has a slightly different, fixed ack latency
    """Return a deterministic, per-replica simulated network round-trip latency in seconds."""  # => documents the contract
    base_latency = 0.02  # => co-07: a baseline 20ms round trip, representative of a same-region network hop
    return base_latency + (replica_index * 0.01)  # => co-07: each ADDITIONAL replica is a LITTLE farther/slower, deterministically


def write_and_wait_for_w_acks(replica_count: int, w: int) -> float:  # => co-07: blocks until W replicas ack, returns elapsed seconds
    """Simulate a write that blocks until W of replica_count replicas ack, returning wall-clock latency."""  # => documents contract
    latencies = sorted(simulate_replica_ack_latency_seconds(i) for i in range(replica_count))  # => co-07: FASTEST replicas ack first, always
    start = time.perf_counter()  # => marks the start of the timed write
    for i in range(w):  # => co-07: the write BLOCKS until exactly W replicas have acked -- the W-th ack determines total latency
        time.sleep(latencies[i])  # => co-07: waits for THIS replica's own simulated ack latency
    return time.perf_counter() - start  # => co-07: total elapsed wall-clock time -- the SUM of each required replica's ack latency, waited in sequence


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    replica_count = 5  # => co-07: N=5 replicas -- large enough to show a clear W=1 vs QUORUM vs ALL spread

    latency_w1 = write_and_wait_for_w_acks(replica_count, w=1)  # => co-07: W=1 -- only the FASTEST replica's ack is required
    latency_quorum = write_and_wait_for_w_acks(replica_count, w=3)  # => co-07: W=QUORUM -- a majority of 5, i.e. 3 replicas
    latency_all = write_and_wait_for_w_acks(replica_count, w=5)  # => co-07: W=ALL -- every one of the 5 replicas must ack

    print(f"W=1:       {latency_w1 * 1000:.1f}ms")  # => Output line -- the fastest of the three, waits for only 1 ack
    print(f"W=QUORUM:  {latency_quorum * 1000:.1f}ms")  # => Output line -- waits for the 3rd-fastest ack
    print(f"W=ALL:     {latency_all * 1000:.1f}ms")  # => Output line -- waits for the SLOWEST replica's ack

    assert latency_w1 < latency_quorum < latency_all  # => co-07: latency STRICTLY increases as W increases -- exactly the tradeoff co-07 names
    print("Latency increases monotonically as W increases: W=1 fastest, W=ALL slowest -- each additional required replica adds its own ack latency in sequence")  # => Output line
    # => co-07: this is the exact mechanism behind the abstract W+R>N math from Example 38 -- a HIGHER W
    # => buys stronger durability guarantees at the direct cost of waiting for a SLOWER replica's ack
    # => on every single write


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
