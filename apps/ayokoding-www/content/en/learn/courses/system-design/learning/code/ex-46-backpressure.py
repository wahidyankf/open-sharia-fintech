# => Use the standard-library helper required by this runnable model.
from queue import Full, Queue


# => Initialize or update deterministic state used by this demonstration.
queue: Queue[str] = Queue(maxsize=1)


# => Isolate the operation so its observable behavior can be checked.
def submit(job: str) -> bool:
    # Non-blocking enqueue makes overload an immediate admission response.
    # => Make the modeled success or overload path explicit.
    try:
        # => Initialize or update deterministic state used by this demonstration.
        queue.put_nowait(job)
        # => Return the observable result of this modeled operation.
        return True
    # => Make the modeled success or overload path explicit.
    except Full:
        # => Return the observable result of this modeled operation.
        return False


# => Check the promised observable behavior of the demonstration.
assert submit("first") is True
# The second job is rejected rather than growing an unbounded in-memory queue.
# => Check the promised observable behavior of the demonstration.
assert submit("second") is False
# => Emit the final observable state for a direct run.
print("bounded queue")
