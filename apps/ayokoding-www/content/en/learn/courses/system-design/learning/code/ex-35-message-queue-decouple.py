# => Use the standard-library helper required by this runnable model.
from queue import Queue


# => Initialize or update deterministic state used by this demonstration.
jobs: Queue[str] = Queue()


# => Isolate the operation so its observable behavior can be checked.
def produce(job: str) -> str:
    # Enqueueing finishes before any consumer performs the slow work.
    # => Initialize or update deterministic state used by this demonstration.
    jobs.put(job)
    # => Return the observable result of this modeled operation.
    return "accepted"


# => Check the promised observable behavior of the demonstration.
assert produce("send-receipt") == "accepted"
# The queued item proves the producer did not wait for consumption.
# => Check the promised observable behavior of the demonstration.
assert jobs.get_nowait() == "send-receipt"
# => Emit the final observable state for a direct run.
print("decoupled")
