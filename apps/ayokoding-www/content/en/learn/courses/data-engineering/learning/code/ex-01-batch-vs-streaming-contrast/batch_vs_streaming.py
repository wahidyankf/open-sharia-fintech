"""Worked Example 1: Batch vs. Streaming Contrast."""  # => co-01: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

ORDER_AMOUNTS = [1200, 450, 890, 3100, 275, 640, 1980, 510]  # => co-01: the SAME eight order amounts, processed two different ways


def batch_total(amounts: list[int]) -> int:  # => co-01: BATCH -- a bounded dataset, processed in one pass
    """Sum a bounded, already-fully-arrived list of amounts in a single pass."""  # => co-01: documents batch_total's contract -- no runtime output, just sets its __doc__
    return sum(amounts)  # => co-01: one call, over the WHOLE dataset, because batch assumes it has already arrived


def streaming_total(amounts: list[int]) -> int:  # => co-01: STREAMING -- an unbounded feed, processed record-by-record
    """Fold an unbounded feed into a running total, one record at a time, as if each just arrived."""  # => co-01: documents streaming_total's contract -- no runtime output, just sets its __doc__
    running_total = 0  # => co-01: the streaming engine's own state -- carried FORWARD between records
    for amount in amounts:  # => co-01: one record at a time -- streaming never assumes the whole feed has arrived
        running_total += amount  # => co-01: update the running aggregate as each record is seen
        print(f"  streaming saw {amount} -> running total {running_total}")  # => co-01: a streaming engine emits a value PER record, not just at the end
    return running_total  # => co-01: returns this computed value to the caller


if __name__ == "__main__":  # => co-01: entry point -- runs only when this file executes directly, not on import
    print(f"Batch pass over {len(ORDER_AMOUNTS)} orders (bounded, arrives all at once):")  # => co-01: frames the batch run
    batch_result = batch_total(ORDER_AMOUNTS)  # => co-01: ONE pass, over the whole bounded dataset
    print(f"  batch total -> {batch_result}")  # => co-01: prints the single, final batch answer

    print(f"Streaming pass over the SAME {len(ORDER_AMOUNTS)} orders (unbounded feed, record-by-record):")  # => co-01
    streaming_result = streaming_total(ORDER_AMOUNTS)  # => co-01: the SAME aggregate, computed incrementally instead
    print(f"  streaming total -> {streaming_result}")  # => co-01: prints the final incrementally-built answer

    assert batch_result == streaming_result, "the same aggregate must match, computed either way"  # => co-01: the whole point
    print(f"MATCH: batch and streaming both compute {batch_result} for the identical eight orders")  # => co-01
    # => co-01: batch waits for the whole bounded set; streaming carries state forward one record at a time -- same answer, different shape
