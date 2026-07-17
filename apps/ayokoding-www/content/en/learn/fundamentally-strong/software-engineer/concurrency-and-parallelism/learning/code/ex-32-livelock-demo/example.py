"""Example 32: Livelock -- Both Threads Active, Neither Makes Progress."""  # => co-17: active but perpetually unproductive

import threading  # => co-17: livelock -- unlike deadlock, both threads keep RUNNING, just uselessly

MAX_TICKS = 30  # => bounded so this demo terminates -- a REAL livelock would run forever


def polite_worker(  # => co-17: runs one "always defer to the other" side of the livelock
    own_wants: list[bool],
    other_wants: list[bool],
    tick_barrier: threading.Barrier,
    progress: list[int],
    # => own_wants/other_wants: each side's per-tick intent flag; progress: shared success counter
) -> None:
    for _ in range(MAX_TICKS):  # => runs a fixed number of synchronized "ticks"
        own_wants[0] = True  # => this thread ALWAYS wants the shared resource, every single tick
        tick_barrier.wait()  # => sync point 1: both threads have now declared their intent for this tick
        if not other_wants[0]:  # => only reached if the other thread did NOT want it this tick (never happens here)
            progress[0] += 1  # => this thread proceeds -- real progress, only possible without contention
        # => deliberately NEVER writes own_wants[0] here: this tick's decision has already been made by
        # => BOTH threads reading the SAME post-barrier1 snapshot (True/True) -- see Discussion below
        tick_barrier.wait()  # => sync point 2: both threads have finished reacting for this tick


if __name__ == "__main__":  # => module entry point
    wants_a = [False]  # => thread A's "I want the resource" flag, read by thread B
    wants_b = [False]  # => thread B's "I want the resource" flag, read by thread A
    barrier = threading.Barrier(2)  # => forces both threads to move through ticks in lockstep
    progress_count = [0]  # => how many ticks resulted in EITHER thread actually proceeding
    t_a = threading.Thread(target=polite_worker, args=(wants_a, wants_b, barrier, progress_count))
    t_b = threading.Thread(target=polite_worker, args=(wants_b, wants_a, barrier, progress_count))
    t_a.start()  # => starts thread A's polite-yielding loop
    t_b.start()  # => starts thread B's polite-yielding loop
    t_a.join(timeout=2)  # => bounded wait -- MAX_TICKS guarantees this finishes well within it
    t_b.join(timeout=2)  # => same bound for thread B

    print(f"progress_count={progress_count[0]} after {MAX_TICKS} ticks")  # => Output: progress_count=0 after 30 ticks

    # => Neither thread is BLOCKED (unlike ex-29's deadlock) -- both are actively running every
    # => tick, checking, and reacting. But because EACH always backs off the instant it sees the
    # => OTHER also wants the resource, and BOTH always want it, neither ever actually proceeds --
    # => this is livelock: active, responsive, and permanently unproductive. An EARLIER version of
    # => this example mutated `own_wants[0] = False` inside the `if` branch to model "backing off" --
    # => but that write raced with the OTHER thread's read of the SAME flag between the two barrier
    # => waits, occasionally letting one thread observe a flag that had already flipped, break the
    # => symmetry, and wrongly "win" a tick. Removing that write (own_wants[0] only ever changes
    # => right before barrier1, never in response to the other's read) makes both reads deterministically
    # => see True/True every tick, with no write racing a read in between -- a genuinely reliable demo.
    assert progress_count[0] == 0  # => confirms zero ticks resulted in either thread making progress
    print("ex-32 OK")  # => Output: ex-32 OK
