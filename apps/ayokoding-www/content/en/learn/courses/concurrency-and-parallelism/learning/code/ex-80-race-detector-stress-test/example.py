"""Example 80: A Stress Harness -- Repeated Trials Surface an Intermittent Race."""

import random  # => co-08: makes the race window trigger only SOMETIMES, not on every single call
import threading  # => co-11: the SAME lock-based fix proven throughout this topic
import time  # => `sleep(0)` is the collision-widening technique, but gated behind a random chance here

TRIALS = 20  # => how many independent trial runs the stress harness performs
ITERATIONS_PER_THREAD = 200  # => how many increments each of the two racing threads attempts, per trial
COLLISION_CHANCE = 0.15  # => the probability, PER INCREMENT, that this call widens the race window at all


def racy_worker(counter: list[int], iterations: int) -> None:  # => the UNSYNCHRONIZED version -- no lock
    for _ in range(iterations):  # => repeats the read-modify-write `iterations` times
        current = counter[0]  # => READ -- no lock protecting this at all
        if random.random() < COLLISION_CHANCE:  # => only SOMETIMES widens the window -- an INTERMITTENT race
            time.sleep(0)  # => yields here, but only on the "unlucky" calls -- most calls stay narrow and safe
        counter[0] = current + 1  # => WRITE BACK -- may or may not overwrite a concurrent update, depending on luck


def locked_worker(counter: list[int], iterations: int, lock: threading.Lock) -> None:  # => the FIX
    for _ in range(iterations):  # => repeats the SAME shape, but fully protected
        with lock:  # => the ENTIRE read-modify-write runs as one atomic critical section, every single time
            current = counter[0]  # => READ -- safe, because the lock excludes the other thread here
            if random.random() < COLLISION_CHANCE:  # => the SAME random widening -- proving the LOCK is what matters
                time.sleep(0)  # => still yields sometimes, but INSIDE the lock -- no other thread can interleave
            counter[0] = current + 1  # => WRITE BACK -- always correct, regardless of the random widening above


def stress_test(worker_is_locked: bool) -> int:  # => returns HOW MANY of the TRIALS observed a lost update
    failures = 0  # => failures: incremented once per trial where the final count is WRONG
    for _ in range(TRIALS):  # => runs TRIALS independent, fresh two-thread races
        counter = [0]  # => a BRAND NEW counter for every trial -- no state leaks between trials
        lock = threading.Lock()  # => a BRAND NEW lock for every trial (used only by the locked variant)
        if worker_is_locked:  # => picks which worker function BOTH threads in this trial will run
            t1 = threading.Thread(target=locked_worker, args=(counter, ITERATIONS_PER_THREAD, lock))
            t2 = threading.Thread(target=locked_worker, args=(counter, ITERATIONS_PER_THREAD, lock))
        else:
            t1 = threading.Thread(target=racy_worker, args=(counter, ITERATIONS_PER_THREAD))
            t2 = threading.Thread(target=racy_worker, args=(counter, ITERATIONS_PER_THREAD))
        t1.start()  # => starts the first racing thread for this trial
        t2.start()  # => starts the second racing thread for this trial
        t1.join()  # => waits for both threads to finish this trial's increments
        t2.join()  # => now safe to check this trial's final counter value
        if counter[0] != 2 * ITERATIONS_PER_THREAD:  # => the CORRECT total, if nothing was ever lost
            failures += 1  # => this trial surfaced a lost update
    return failures  # => how many of the TRIALS actually exhibited the race


if __name__ == "__main__":  # => module entry point
    racy_failures = stress_test(worker_is_locked=False)  # => racy_failures: how many trials the UNSYNCHRONIZED version lost
    locked_failures = stress_test(worker_is_locked=True)  # => locked_failures: how many trials the LOCKED version lost
    print(f"racy_failures={racy_failures}/{TRIALS} locked_failures={locked_failures}/{TRIALS}")
    # => Output: racy_failures=<some number > 0>/20 locked_failures=0/20

    # => A race that only manifests occasionally is FAR more dangerous in practice than an always-broken
    # => one, precisely because a SINGLE test run can pass by pure luck (co-08) -- this is why real race
    # => detectors and CI harnesses run the SAME racy code many times under load (a "stress test") rather
    # => than trusting one green run. Here, a single trial might easily show the correct total by chance;
    # => repeating it TRIALS times reliably surfaces at least one failure for the unlocked version, while
    # => the SAME stress harness applied to the lock-protected version (co-11) NEVER fails, across every trial.
    assert racy_failures > 0  # => confirms the stress harness DID surface the race in at least one trial
    assert locked_failures == 0  # => confirms the lock-protected version passed EVERY single trial
    print("ex-80 OK")  # => Output: ex-80 OK
