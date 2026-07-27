"""Worked Example 51: The Same Retry, Against an Idempotent Merge-on-Key Sink."""  # => co-21: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


class IdempotentMergeSink:  # => co-21: models a sink whose write is a MERGE on a dedup key, not a plain append
    """A sink that merges by order_id -- a retry of the SAME record updates in place, never duplicating."""  # => co-21: documents IdempotentMergeSink's contract -- no runtime output, just sets its __doc__

    def __init__(self) -> None:  # => co-21: sets up this sink's own key-indexed storage
        self.rows_by_key: dict[int, dict[str, object]] = {}  # => co-21: order_id -> row -- a dict, not a list, is what MAKES this idempotent

    def write(self, record: dict[str, object]) -> None:  # => co-21: MERGE, not append -- exactly the co-05 upsert mechanism, applied at the sink
        self.rows_by_key[record["order_id"]] = dict(record)  # => co-21: overwrites in place on the SAME key -- a retry changes nothing observable


def exactly_once_processing_result(order_id: int) -> dict[str, object]:  # => co-21: the SAME engine-side result ex-50 computed
    """Simulate an engine's exactly-once-processed output for one order."""  # => co-21: documents exactly_once_processing_result's contract -- no runtime output, just sets its __doc__
    return {"order_id": order_id, "status": "processed"}  # => co-21: identical shape to ex-50 -- only the SINK differs between the two examples


if __name__ == "__main__":  # => co-21: entry point -- runs only when this file executes directly, not on import
    sink = IdempotentMergeSink()  # => co-21: a fresh, MERGE-based sink -- keyed by order_id
    result = exactly_once_processing_result(order_id=8002)  # => co-21: the SAME kind of engine-computed result ex-50 used
    sink.write(result)  # => co-21: the FIRST write -- a normal, successful delivery
    print(f"After the first write: {sink.rows_by_key}")  # => co-21: prints the sink's state after one write

    sink.write(result)  # => co-21: the SAME retry scenario ex-50 demonstrated -- but THIS sink merges on order_id
    print(f"After the retry write (same record): {sink.rows_by_key}")  # => co-21: prints the sink's state after the retry

    row_count = len(sink.rows_by_key)  # => co-21: how many DISTINCT rows actually landed at the sink
    print(f"Rows at the sink after engine-exactly-once processing PLUS one retry: {row_count}")  # => co-21: prints the count
    assert row_count == 1, "an idempotent merge-on-key sink must land the SAME retried record exactly once"  # => co-21: the claim ex-51 makes
    print("MATCH: the identical retry that duplicated at ex-50's sink lands exactly once here, thanks to the merge key")  # => co-21
    # => co-21: making the SINK write idempotent (merge on a natural/dedup key) is what closes the gap engine-exactly-once alone cannot
