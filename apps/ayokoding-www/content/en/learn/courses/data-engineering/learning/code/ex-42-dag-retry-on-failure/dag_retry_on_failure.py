"""Worked Example 42: DAG Retry on Failure."""  # => co-18: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

MAX_RETRIES = 3  # => co-18: Airflow's own default_args-style retry budget for a task


class FlakyTask:  # => co-18: a task that fails on its first two attempts, then succeeds -- a realistic transient-failure shape
    """A task that fails its first two attempts, then succeeds on the third."""  # => co-18: documents FlakyTask's contract -- no runtime output, just sets its __doc__

    def __init__(self) -> None:  # => co-18: tracks how many times this task has actually been attempted
        self.attempt_count = 0  # => co-18: starts at zero -- no attempts yet

    def run(self) -> str:  # => co-18: one attempt -- raises on the first two calls, succeeds on the third
        self.attempt_count += 1  # => co-18: record this attempt, whether it succeeds or not
        if self.attempt_count < 3:  # => co-18: attempts 1 and 2 both fail -- a genuinely flaky upstream dependency
            raise RuntimeError(f"transient failure on attempt {self.attempt_count}")  # => co-18: simulates a real, recoverable failure
        return "success"  # => co-18: attempt 3 succeeds


def run_with_retries(task: FlakyTask, *, max_retries: int) -> str:  # => co-18: the scheduler's own retry-policy loop
    """Retry `task.run()` up to max_retries times, re-raising only if every attempt fails."""  # => co-18: documents run_with_retries's contract -- no runtime output, just sets its __doc__
    last_error: Exception | None = None  # => co-18: remembers the most recent failure, for re-raising if all retries are exhausted
    for attempt in range(1, max_retries + 1):  # => co-18: attempt 1 through max_retries, inclusive
        try:  # => co-18: one retry attempt
            return task.run()  # => co-18: SUCCESS -- return immediately, no further retries needed
        except RuntimeError as error:  # => co-18: this attempt failed -- record it and try again
            last_error = error  # => co-18: keep the most recent failure's details
            print(f"  attempt {attempt} failed: {error}")  # => co-18: log every failed attempt, matching a real scheduler's retry log
    raise RuntimeError("exhausted all retries") from last_error  # => co-18: re-raised only if EVERY attempt failed


if __name__ == "__main__":  # => co-18: entry point -- runs only when this file executes directly, not on import
    flaky_task = FlakyTask()  # => co-18: a fresh flaky task, zero attempts so far
    result = run_with_retries(flaky_task, max_retries=MAX_RETRIES)  # => co-18: retries automatically, per Airflow's default_args-style policy
    print(f"Final result: {result!r} | Total attempts made: {flaky_task.attempt_count}")  # => co-18: prints the outcome and attempt count

    assert result == "success", "the task must succeed once it eventually succeeds within the retry budget"  # => co-18: the claim
    assert flaky_task.attempt_count == 3, "exactly three attempts must have been made -- two failures, one success"  # => co-18
    print(f"MATCH: the task succeeded on attempt {flaky_task.attempt_count}, within the {MAX_RETRIES}-retry budget")  # => co-18
    # => co-18: a retry policy is what lets a genuinely transient failure resolve itself instead of failing the whole DAG run
