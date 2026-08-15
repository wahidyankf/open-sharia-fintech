# => Use the standard-library helper required by this runnable model.
from collections import deque


# => Isolate the operation so its observable behavior can be checked.
def distribute(jobs: list[str], workers: list[str]) -> dict[str, list[str]]:
    # A deque models the shared work source.
    # => Initialize or update deterministic state used by this demonstration.
    pending, assigned = deque(jobs), {worker: [] for worker in workers}
    # => Repeat the deterministic step over the current input.
    while pending:
        # Each turn gives one available worker the next independent job.
        # => Repeat the deterministic step over the current input.
        for worker in workers:
            # => Choose the branch that models this design condition.
            if pending:
                # => Initialize or update deterministic state used by this demonstration.
                assigned[worker].append(pending.popleft())
    # => Return the observable result of this modeled operation.
    return assigned


# => Initialize or update deterministic state used by this demonstration.
result = distribute(["a", "b", "c", "d"], ["one", "two"])
# Equal-duration jobs split evenly in this deterministic schedule.
# => Check the promised observable behavior of the demonstration.
assert [len(items) for items in result.values()] == [2, 2]
# => Emit the final observable state for a direct run.
print(result)
