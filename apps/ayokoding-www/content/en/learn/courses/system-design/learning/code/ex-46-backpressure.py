from queue import Full, Queue


queue: Queue[str] = Queue(maxsize=1)


def submit(job: str) -> bool:
    # Non-blocking enqueue makes overload an immediate admission response.
    try:
        queue.put_nowait(job)
        return True
    except Full:
        return False


assert submit("first") is True
# The second job is rejected rather than growing an unbounded in-memory queue.
assert submit("second") is False
print("bounded queue")
