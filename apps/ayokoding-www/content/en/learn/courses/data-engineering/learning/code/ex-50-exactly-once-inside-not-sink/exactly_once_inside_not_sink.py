"""Worked Example 50: Exactly-Once Inside the Engine, Not at the Sink."""  # => co-21: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


class NonIdempotentSink:  # => co-21: models a sink whose write is a plain APPEND -- no dedup, no merge key
    """A sink that appends unconditionally -- every write() call adds a NEW row, even a retry of the same one."""  # => co-21: documents NonIdempotentSink's contract -- no runtime output, just sets its __doc__

    def __init__(self) -> None:  # => co-21: sets up this sink's own append-only storage
        self.rows: list[dict[str, object]] = []  # => co-21: every row ever written, in order, no dedup applied anywhere

    def write(self, record: dict[str, object]) -> None:  # => co-21: an unconditional append -- the exact failure mode this example demonstrates
        self.rows.append(dict(record))  # => co-21: appends REGARDLESS of whether this exact record was already written before


def exactly_once_processing_result(order_id: int) -> dict[str, object]:  # => co-21: stands in for an engine's own EXACTLY-ONCE-processed result
    """Simulate an engine's exactly-once-processed output for one order -- INSIDE the engine, this is computed exactly once."""  # => co-21: documents exactly_once_processing_result's contract -- no runtime output, just sets its __doc__
    return {"order_id": order_id, "status": "processed"}  # => co-21: the engine's own internal guarantee -- one canonical result per order


if __name__ == "__main__":  # => co-21: entry point -- runs only when this file executes directly, not on import
    sink = NonIdempotentSink()  # => co-21: a fresh, non-idempotent sink -- no merge key, no dedup
    result = exactly_once_processing_result(order_id=8001)  # => co-21: the engine's exactly-once-computed result -- computed ONCE, internally
    sink.write(result)  # => co-21: the FIRST write -- a normal, successful delivery to the sink
    print(f"After the first write: {sink.rows}")  # => co-21: prints the sink's state after one write

    sink.write(result)  # => co-21: a RETRY of the SAME already-written result -- e.g. the sink ack was lost, so the pipeline retried
    print(f"After the retry write (same record): {sink.rows}")  # => co-21: prints the sink's state after the retry

    row_count = len(sink.rows)  # => co-21: how many rows actually landed at the sink
    print(f"Rows at the sink after engine-exactly-once processing PLUS one retry: {row_count}")  # => co-21: prints the count
    assert row_count == 2, "a non-idempotent sink must double-write on a retry, even though the ENGINE processed exactly once"  # => co-21: the claim
    print("MATCH: the engine computed the result exactly once, but the non-idempotent sink still wrote it TWICE")  # => co-21
    # => co-21: exactly-once INSIDE the engine says nothing about the SINK -- the sink write must itself be made idempotent (co-21's next example)
