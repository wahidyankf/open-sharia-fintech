from collections import deque


def distribute(jobs: list[str], workers: list[str]) -> dict[str, list[str]]:
    # A deque models the shared work source.
    pending, assigned = deque(jobs), {worker: [] for worker in workers}
    while pending:
        # Each turn gives one available worker the next independent job.
        for worker in workers:
            if pending:
                assigned[worker].append(pending.popleft())
    return assigned


result = distribute(["a", "b", "c", "d"], ["one", "two"])
# Equal-duration jobs split evenly in this deterministic schedule.
assert [len(items) for items in result.values()] == [2, 2]
print(result)
