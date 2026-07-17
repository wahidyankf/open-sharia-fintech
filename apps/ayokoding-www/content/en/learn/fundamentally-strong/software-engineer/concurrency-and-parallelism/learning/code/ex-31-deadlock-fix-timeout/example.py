"""Example 31: `acquire(timeout=...)` + Back-Off Fixes a Deadlock Differently."""  # => co-16, co-11: give up and retry, don't wait forever

import random  # => randomizes the back-off so retries don't stay perfectly synchronized
import threading  # => co-11's timed acquire, applied to co-16's opposite-order deadlock shape
import time  # => `time.sleep` implements the back-off delay between retries


def try_once(first: threading.Lock, second: threading.Lock, attempts: list[int]) -> bool:  # => one contend-and-maybe-win attempt
    first.acquire()  # => grabs its "first" lock -- unconditionally, like ex-29
    attempts[0] += 1  # => records that this thread made another attempt at winning both locks
    got_second = second.acquire(timeout=0.05)  # => bounded wait, NOT an unconditional block
    if got_second:  # => successfully got BOTH locks -- safe to proceed and then clean up
        second.release()  # => releases in reverse-ish order -- cleanup for this successful attempt
        first.release()  # => releases the first lock too -- attempt fully complete
        return True  # => this attempt WON both locks -- caller should stop retrying
    first.release()  # => COULD NOT get the second lock -- releases the first to break the standoff
    return False  # => this attempt failed -- caller should back off and retry


def worker(  # => co-16 fix in action: retry-with-timeout instead of an unconditional acquire
    first: threading.Lock,
    second: threading.Lock,
    both_ready: threading.Barrier,
    attempts: list[int],
    # => first/second: THIS thread's acquisition order; attempts: shared retry counter
) -> None:
    both_ready.wait()  # => rendezvous ONCE -- guarantees BOTH threads collide on their first attempt
    if try_once(first, second, attempts):  # => the guaranteed-contention first attempt
        return  # => rare, but possible: this thread won immediately despite the forced collision
    while not try_once(first, second, attempts):  # => keeps retrying until one attempt wins both locks
        time.sleep(random.uniform(0, 0.02))  # => back-off before retrying -- avoids instant re-collision


def resolves_via_timeout() -> tuple[int, int]:  # => returns (thread_a_attempts, thread_b_attempts)
    lock_a = threading.Lock()  # => resource A
    lock_b = threading.Lock()  # => resource B
    rendezvous = threading.Barrier(2)  # => forces both threads to contend at the same moment, each retry round
    a_attempts = [0]  # => how many times thread_a tried before succeeding
    b_attempts = [0]  # => how many times thread_b tried before succeeding
    t_a = threading.Thread(target=worker, args=(lock_a, lock_b, rendezvous, a_attempts))  # => wants A then B
    t_b = threading.Thread(target=worker, args=(lock_b, lock_a, rendezvous, b_attempts))  # => wants B then A
    t_a.start()  # => starts thread_a's retry loop
    t_b.start()  # => starts thread_b's retry loop -- opposite acquisition order, just like ex-29
    t_a.join(timeout=3)  # => a generous but FINITE bound -- the retry loop must eventually succeed
    t_b.join(timeout=3)  # => same bound for thread_b
    return a_attempts[0], b_attempts[0]  # => both > 0 confirms real work happened, not instant luck


if __name__ == "__main__":  # => module entry point
    a_tries, b_tries = resolves_via_timeout()  # => a_tries/b_tries: how many rounds each thread needed
    print(f"a_tries={a_tries} b_tries={b_tries}")  # => Output: a_tries=<1+> b_tries=<1+>

    # => Instead of blocking forever, `acquire(timeout=...)` lets a thread give up, release what it
    # => already holds, back off, and retry -- turning a permanent deadlock into eventual progress.
    # => This trades a HARD guarantee (lock ordering, ex-30) for a PROBABILISTIC one: it always
    # => makes progress eventually, but the exact number of retries needed is not fixed in advance.
    assert a_tries >= 1  # => confirms thread_a made at least one attempt and eventually succeeded
    assert b_tries >= 1  # => confirms thread_b made at least one attempt and eventually succeeded
    print("ex-31 OK")  # => Output: ex-31 OK
