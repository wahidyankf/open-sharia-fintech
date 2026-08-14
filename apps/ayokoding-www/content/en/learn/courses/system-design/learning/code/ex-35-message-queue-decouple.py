from queue import Queue


jobs: Queue[str] = Queue()


def produce(job: str) -> str:
    # Enqueueing finishes before any consumer performs the slow work.
    jobs.put(job)
    return "accepted"


assert produce("send-receipt") == "accepted"
# The queued item proves the producer did not wait for consumption.
assert jobs.get_nowait() == "send-receipt"
print("decoupled")
