"""Kata 10 (before): a single shared dict lets one worker's "current request" bleed into another's."""

import threading
import time

request_context: dict[str, str] = {}  # SMELL: ONE shared dict for "the current request", used by every thread


def handle_request(worker_name: str, request_id: str, delay_before_read: float, observed: dict[str, str]) -> None:
    request_context["request_id"] = request_id  # BUG: overwrites the SAME shared key every worker touches
    time.sleep(delay_before_read)  # => simulates request-handling work happening before the read below
    observed[worker_name] = request_context["request_id"]  # => reads back whatever is CURRENTLY there


observed: dict[str, str] = {}
# => worker_slow sets its ID, THEN sleeps -- worker_fast sets ITS OWN id and finishes reading first,
# => overwriting the shared key while worker_slow is still asleep, before worker_slow ever reads back.
worker_slow = threading.Thread(target=handle_request, args=("worker_slow", "REQ-A", 0.15, observed))
worker_fast = threading.Thread(target=handle_request, args=("worker_fast", "REQ-B", 0.0, observed))
worker_slow.start()
time.sleep(0.02)  # => lets worker_slow set REQ-A into the shared dict before worker_fast starts
worker_fast.start()
worker_slow.join()
worker_fast.join()
print(observed)
# => worker_slow ASKED for "REQ-A" but, because worker_fast overwrote the ONE shared key while
# => worker_slow was still asleep, worker_slow's own read-back sees "REQ-B" instead -- state bled
# => across threads through the single shared dict.
assert observed["worker_slow"] == "REQ-B"  # => confirms the WRONG, bled-over value was observed
assert observed["worker_fast"] == "REQ-B"  # => worker_fast correctly sees its own id
print("kata OK (bug reproduced)")
