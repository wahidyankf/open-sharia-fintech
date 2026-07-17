"""Example 71: Work-Stealing -- an Idle Worker Steals From an Overloaded Peer's Deque."""

from collections import deque  # => co-28: the classic data structure behind work-stealing schedulers


def simulate_work_stealing(worker_a: "deque[int]", worker_b: "deque[int]") -> tuple[int, int, list[str]]:  # => a single-threaded SKETCH of the idea -- deterministic, not a race
    completed_a = 0  # => completed_a: how many tasks worker "a" ends up processing, own OR stolen
    completed_b = 0  # => completed_b: how many tasks worker "b" ends up processing, own OR stolen
    steal_events: list[str] = []  # => steal_events: a log of every time one worker stole from the other

    while worker_a or worker_b:  # => keeps going until BOTH deques are fully drained
        if worker_a:  # => worker "a" has its OWN work -- processes from its OWN end (locality, low contention)
            worker_a.pop()  # => pops from the RIGHT end -- the owner's "local" end of its own deque
            completed_a += 1  # => counts one task processed by worker "a"
        elif worker_b:  # => worker "a" is IDLE -- its own deque is empty, but worker "b" still has work
            worker_b.popleft()  # => STEALS from the LEFT end -- the opposite end from "b"'s own popping
            completed_a += 1  # => the STOLEN task still counts toward worker "a"'s own completed total
            steal_events.append("a<-b")  # => records that "a" stole from "b" this round

        if worker_b:  # => worker "b" has its OWN work -- same local-end popping as worker "a" above
            worker_b.pop()  # => pops from the RIGHT end -- worker "b"'s own local end
            completed_b += 1  # => counts one task processed by worker "b"
        elif worker_a:  # => worker "b" is IDLE -- symmetric to the "a" branch above
            worker_a.popleft()  # => STEALS from the LEFT end of worker "a"'s deque
            completed_b += 1  # => the STOLEN task counts toward worker "b"'s own completed total
            steal_events.append("b<-a")  # => records that "b" stole from "a" this round

    return completed_a, completed_b, steal_events  # => everything needed to verify the load actually balanced


if __name__ == "__main__":  # => module entry point
    worker_a_tasks: "deque[int]" = deque(range(2))  # => worker "a" starts with only 2 tasks -- WILL run out fast
    worker_b_tasks: "deque[int]" = deque(range(18))  # => worker "b" starts with 18 tasks -- deliberately OVERLOADED
    completed_a, completed_b, steal_events = simulate_work_stealing(worker_a_tasks, worker_b_tasks)
    print(f"completed_a={completed_a} completed_b={completed_b} steal_count={len(steal_events)}")
    # => Output: completed_a=10 completed_b=10 steal_count=8

    total_tasks = 2 + 18  # => total_tasks: the mathematically correct grand total, from BOTH initial deques
    # => the exact 8/12 split above comes from this simulation's own deterministic round-robin order

    # => Without stealing, worker "a" would finish its 2 tasks almost instantly and then sit COMPLETELY
    # => idle while worker "b" churns through 18 tasks alone -- a wasted core. Work-stealing lets an idle
    # => worker grab tasks from an OVERLOADED peer's deque instead (co-28), and popping from OPPOSITE ends
    # => (owner: local end; thief: far end) minimizes contention between the two, since they rarely reach
    # => for the same slot. The result: BOTH workers stay busy, and the total work still gets fully done.
    assert completed_a + completed_b == total_tasks  # => confirms every task was processed exactly once
    assert completed_a > 2  # => confirms worker "a" processed MORE than its own original 2 tasks -- it stole work
    assert len(steal_events) > 0  # => confirms stealing genuinely happened, not just idle waiting
    print("ex-71 OK")  # => Output: ex-71 OK
