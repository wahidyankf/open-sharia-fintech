# pyright: strict
"""Example 57: Queue -- produce a job, consume it once. (co-28)

A simple in-process queue: a producer enqueues a job, a worker consumes it
and acks. The job runs exactly once in the happy path. This sets up the
at-least-once redelivery failure mode of Example 58.
"""

from collections import deque  # => deque: a simple FIFO queue
from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-28: one unit of background work
class Job:
    id: int  # => the job's id
    payload: str  # => what the worker should do


@dataclass  # => co-28: a tiny broker + worker
class Queue:
    pending: deque[Job] = field(default_factory=deque[Job])  # => jobs waiting to be consumed
    processed: list[int] = field(default_factory=list[int])  # => ids of jobs the worker acked

    def produce(self, job: Job) -> None:  # => enqueue a job
        self.pending.append(job)  # => FIFO: to the back

    def consume_once(self) -> int | None:  # => the worker pulls ONE job and acks it
        if not self.pending:  # => nothing to do
            return None  # => idle
        job = self.pending.popleft()  # => pull the front job
        self.processed.append(job.id)  # => co-28: the ACK -- records this job as done
        return job.id  # => the job that ran


q = Queue()  # => co-28: one queue + worker
q.produce(Job(1, "send email"))  # => enqueue job 1
q.produce(Job(2, "resize image"))  # => enqueue job 2
print(f"pending before consume: {[j.id for j in q.pending]}")  # => Output: [1, 2]

ran = q.consume_once()  # => co-28: the worker runs job 1 and acks it
print(f"ran job: {ran}, processed: {q.processed}")  # => Output: 1, [1]
print(f"pending after one consume: {[j.id for j in q.pending]}")  # => Output: [2]

assert ran == 1 and q.processed == [1]  # => co-28: the job ran exactly once (happy path)
