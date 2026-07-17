"""Kata 4 (after): a `while` guard keeps waiting until BOTH conditions are actually true."""

import threading
import time

state = {"oven_preheated": False, "dough_ready": False}
cond = threading.Condition()


def baker_waits_for_both(log: list[str]) -> None:
    with cond:
        while not (state["oven_preheated"] and state["dough_ready"]):  # FIX: `while`, RE-checked on every wake
            cond.wait()  # => on an early/partial notify, the predicate is still False, so it waits AGAIN
        log.append(f"baking: oven={state['oven_preheated']} dough={state['dough_ready']}")


def controller_signals_progress() -> None:
    with cond:
        state["oven_preheated"] = True  # => step 1: only the oven becomes ready
        cond.notify_all()  # => an early notify -- the `while` guard correctly ignores it and re-waits
    time.sleep(0.05)  # => gives the baker time to re-check and go back to cond.wait()
    with cond:
        state["dough_ready"] = True  # => step 2: NOW the real predicate becomes true
        cond.notify_all()  # => this notify actually satisfies the `while` condition


log: list[str] = []
waiter = threading.Thread(target=baker_waits_for_both, args=(log,))
waiter.start()
time.sleep(0.05)  # => gives the waiter time to reach cond.wait() before the controller signals
controller_signals_progress()
waiter.join(timeout=1.0)
print(log)
assert log == ["baking: oven=True dough=True"]  # => confirms baking only started once BOTH were ready
print("kata OK (fix verified)")
