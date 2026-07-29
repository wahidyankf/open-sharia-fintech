# pyright: strict
"""Example 6: 202 Accepted for a Long-Running Operation. (co-07)

A long-running operation cannot finish inside one request/response cycle, so
the API accepts the request immediately with `202 Accepted` plus a status
URL, and the caller polls that URL until the job finishes.
"""

from dataclasses import dataclass  # => a small typed response record for this example

JOBS: dict[str, str] = {}  # => job id -> status ("pending" | "done"), the async job's state


@dataclass  # => co-07: the two facts a poll or a kickoff call returns
class Response:
    status: int  # => the HTTP status code
    body: dict[str, str]  # => a small JSON-shaped payload


def start_export(job_id: str) -> Response:  # => POST /exports -- kicks off a slow job
    JOBS[job_id] = "pending"  # => co-07: the job starts in "pending", NOT finished yet
    return Response(status=202, body={"status_url": f"/exports/{job_id}"})  # => 202 + status URL
    # => the caller never blocks waiting for the job -- it gets a URL to check back on


def poll_export(job_id: str) -> Response:  # => GET /exports/{id} -- the status URL from above
    state = JOBS[job_id]  # => reads the CURRENT state, whatever it is right now
    return Response(status=200, body={"state": state})  # => polling itself always succeeds (200)


start = start_export("job-1")  # => call 1: kicks off the job
print(f"start: status={start.status}, body={start.body}")  # => Output: 202, status_url given

poll_1 = poll_export("job-1")  # => call 2: poll immediately -- job hasn't finished yet
print(f"poll (before done): {poll_1.body}")  # => Output: {'state': 'pending'}

JOBS["job-1"] = "done"  # => simulates the background worker finishing the job
poll_2 = poll_export("job-1")  # => call 3: poll again -- now it has finished
print(f"poll (after done): {poll_2.body}")  # => Output: {'state': 'done'}
# => same status_url, two different bodies -- polling is how 202's promise gets fulfilled
