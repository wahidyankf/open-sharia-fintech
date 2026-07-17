"""Example 42: `as_completed` Yields Results in FINISH Order, Not Submit Order."""

import time  # => gives each task a DIFFERENT duration, so finish order differs from submit order
from concurrent.futures import Future, ThreadPoolExecutor, as_completed  # => co-23, co-25

DELAYS = [0.15, 0.01, 0.10, 0.05]  # => task i sleeps DELAYS[i] seconds -- deliberately out of order


def slow_task(task_id: int, delay: float) -> tuple[int, float]:  # => task_id: which task; delay: how long it sleeps
    time.sleep(delay)  # => simulates variable-length work -- task 1 (delay=0.01) finishes FIRST
    return task_id, delay  # => returns identifying info so the caller can match results to submissions


if __name__ == "__main__":  # => module entry point
    with ThreadPoolExecutor(max_workers=4) as pool:  # => 4 workers -- enough for all 4 tasks to run concurrently
        futures: list[Future[tuple[int, float]]] = [pool.submit(slow_task, i, delay) for i, delay in enumerate(DELAYS)]  # => futures: submitted in task_id order 0,1,2,3 -- submit ORDER, not finish order

        submit_order_ids = list(range(len(DELAYS)))  # => submit_order_ids: [0, 1, 2, 3] -- how they were queued
        completion_order_ids: list[int] = []  # => completion_order_ids: filled in FINISH order, below
        for finished_future in as_completed(futures):  # => yields each Future the INSTANT it completes
            task_id, delay = finished_future.result()  # => .result() is immediate here -- the future is already done
            completion_order_ids.append(task_id)  # => records the order results actually arrived in

    print(f"submit_order={submit_order_ids}")  # => Output: submit_order=[0, 1, 2, 3]
    print(f"completion_order={completion_order_ids}")  # => Output: completion_order=[1, 3, 2, 0] (fastest delay first)

    # => `as_completed` yields Futures in the order they FINISH, not the order they were submitted --
    # => task 1 (0.01s delay) finishes before task 0 (0.15s delay) even though task 0 was submitted
    # => first. This matters when later results should be processed as soon as they're ready, rather
    # => than forcing the caller to wait for an EARLIER-submitted-but-SLOWER task before seeing a
    # => later, faster one (contrast with `ThreadPoolExecutor.map`, which preserves submit order).
    assert completion_order_ids != submit_order_ids  # => confirms the orders genuinely differ
    assert set(completion_order_ids) == set(submit_order_ids)  # => confirms every task DID complete, just reordered
    assert completion_order_ids[0] == 1  # => task 1 has the SHORTEST delay -- it must finish first
    print("ex-42 OK")  # => Output: ex-42 OK
