"""Example 65: Cancelling a PENDING `Future` -- Before It Ever Starts."""

import threading  # => coordinates the "occupy the only worker" trick below
from concurrent.futures import Future, ThreadPoolExecutor  # => co-25, co-23: Futures support `.cancel()`

ran_flag = [False]  # => ran_flag[0]: flips to True ONLY if the cancelled task's body actually executes


def occupy_the_only_worker(release_event: threading.Event) -> str:  # => keeps the SINGLE worker busy
    release_event.wait(timeout=2)  # => blocks until the main thread says it's safe to finish
    return "occupier done"  # => only returned once release_event is set


def never_should_run() -> str:  # => the task we intend to cancel BEFORE it ever gets a worker
    ran_flag[0] = True  # => if this line EVER executes, cancellation failed
    return "should never see this"  # => this return value should never be observed either


if __name__ == "__main__":  # => module entry point
    with ThreadPoolExecutor(max_workers=1) as pool:  # => EXACTLY one worker -- forces the second task to QUEUE
        release_event = threading.Event()  # => release_event: lets the main thread control WHEN the occupier finishes
        occupier: Future[str] = pool.submit(occupy_the_only_worker, release_event)  # => grabs the ONLY worker immediately
        pending_future: Future[str] = pool.submit(never_should_run)  # => has NO worker available -- stays PENDING

        cancelled = pending_future.cancel()  # => attempts to cancel it WHILE it's still PENDING, not yet running
        print(f"cancelled={cancelled}")  # => Output: cancelled=True

        release_event.set()  # => now lets the occupier finish, freeing the pool's only worker
        occupier_result = occupier.result()  # => waits for the occupier to actually complete
        print(f"occupier_result={occupier_result!r}")  # => Output: occupier_result='occupier done'

    print(f"ran_flag={ran_flag[0]}")  # => Output: ran_flag=False

    # => A `Future` can only be cancelled successfully while it is still PENDING -- queued, but not yet
    # => handed to a worker thread (co-25). By deliberately occupying the pool's ONLY worker first, this
    # => guarantees `pending_future` has nowhere to run, so `.cancel()` (co-23) reliably succeeds and the
    # => task body never executes at all. Once a task has actually STARTED running, `.cancel()` returns
    # => False instead -- Python's stdlib does not support interrupting an already-running thread mid-task.
    assert cancelled is True  # => confirms the cancellation itself was accepted
    assert ran_flag[0] is False  # => confirms the cancelled task's body genuinely never ran
    assert pending_future.cancelled() is True  # => confirms the Future reports itself as cancelled
    print("ex-65 OK")  # => Output: ex-65 OK
