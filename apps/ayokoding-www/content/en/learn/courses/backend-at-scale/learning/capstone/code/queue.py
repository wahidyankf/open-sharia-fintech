# pyright: strict
"""Capstone Step 4: idempotent queue consumer + integration/contract suite. (co-28, co-29, co-35)

Adds a background-job queue consumer with idempotent processing (co-28
at-least-once delivery, co-29 idempotent dedup), and an integration +
contract test suite (co-35) that verifies duplicate messages process once.
This closes the capstone's four-step arc into a runnable, verified whole.
"""

from collections import deque  # => deque: the at-least-once queue
from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => one background-job message
class Job:
    id: str  # => co-29: the dedup key (stable across redeliveries)
    order_id: int  # => the work to do (e.g. "fulfill this order")


@dataclass  # => co-28: an at-least-once queue + an idempotent consumer
class JobQueue:
    ready: deque[Job] = field(
        default_factory=deque[Job]
    )  # => messages awaiting delivery
    processed: set[str] = field(
        default_factory=set[str]
    )  # => co-29: ids whose effect was applied
    fulfilled: list[int] = field(
        default_factory=list[int]
    )  # => order_ids actually fulfilled (the side effect)

    def enqueue(self, job: Job) -> None:  # => add a job
        self.ready.append(job)  # => to the back

    def deliver(self) -> Job | None:  # => hand one job to the consumer
        if not self.ready:  # => nothing ready
            return None  # => idle
        return self.ready.popleft()  # => the front job

    def requeue(
        self, job: Job
    ) -> None:  # => co-28: redeliver (a failed/unacked job goes back)
        self.ready.append(job)  # => co-28: at-least-once -> may be seen again

    def consume(self, job: Job) -> str:  # => co-29: idempotent processing
        if job.id in self.processed:  # => co-29: duplicate -> skip the side effect
            return "skipped"  # => no effect
        self.processed.add(job.id)  # => record the id
        self.fulfilled.append(job.order_id)  # => apply the side effect ONCE
        return "applied"  # => fulfilled


def run_suite() -> list[
    tuple[str, bool]
]:  # => co-35: an integration + contract test suite
    results: list[tuple[str, bool]] = []  # => per-test pass/fail

    # Integration test: a job is processed, then redelivered (at-least-once), dedup keeps it once.
    q = JobQueue()  # => a fresh queue
    job = Job(id="job-1", order_id=42)  # => one genuine job
    q.enqueue(job)  # => produce
    delivered = q.deliver()  # => co-28: deliver to the consumer
    assert delivered is not None  # => type-narrow
    first = q.consume(delivered)  # => co-29: applied
    q.requeue(delivered)  # => co-28: simulate a redelivery (crash before ack)
    redelivered = q.deliver()  # => co-28: the SAME job handed over again
    assert redelivered is not None  # => type-narrow
    second = q.consume(redelivered)  # => co-29: duplicate -> skipped
    results.append(
        (
            "at-least-once + idempotent consumer",
            first == "applied" and second == "skipped",
        )
    )  # => co-28/co-29
    results.append(
        ("side effect applied exactly once", q.fulfilled == [42])
    )  # => co-29: effect once

    # Contract test: the consumer's effect-once guarantee holds across N redeliveries.
    q2 = JobQueue()  # => a fresh queue
    j = Job(id="job-2", order_id=99)  # => another job
    outcomes: list[str] = []  # => results across N redeliveries
    q2.enqueue(j)  # => produce
    for _ in range(5):  # => co-28: delivered 5 times (at-least-once, many retries)
        d = q2.deliver()  # => deliver
        if d is None:  # => queue drained for this round
            q2.requeue(j)  # => put it back to simulate another redelivery
            continue  # => next iteration
        outcomes.append(q2.consume(d))  # => co-29: applied once, then skipped
        q2.requeue(d)  # => co-28: redeliver again
    results.append(
        ("contract: applied once despite 5 deliveries", outcomes.count("applied") == 1)
    )  # => co-29/co-35
    return results  # => the suite's report


report = run_suite()  # => co-35: run the suite
for name, passed in report:  # => print each test
    print(f"{'PASS' if passed else 'FAIL'}: {name}")  # => Output: three PASS lines

all_green = all(passed for _name, passed in report)  # => the suite verdict
print(f"SUITE: {'GREEN' if all_green else 'RED'}")  # => Output: GREEN
assert all_green  # => co-28/co-29/co-35: duplicate messages process once, suite green
