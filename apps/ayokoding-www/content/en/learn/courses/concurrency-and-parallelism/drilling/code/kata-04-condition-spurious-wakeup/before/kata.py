"""Kata 4 (before): an `if` guard proceeds on the FIRST notify, even before the real predicate is true."""

import threading
import time

state = {"oven_preheated": False, "dough_ready": False}
cond = threading.Condition()


def baker_waits_for_both(log: list[str]) -> None:
    with cond:
        if not (state["oven_preheated"] and state["dough_ready"]):  # SMELL: `if`, checked only ONCE
            cond.wait()  # => wakes on ANY notify_all(), not specifically "both conditions are true"
        # BUG: proceeds here even if only ONE of the two conditions actually became true
        log.append(f"baking: oven={state['oven_preheated']} dough={state['dough_ready']}")


def controller_signals_progress() -> None:
    with cond:
        state["oven_preheated"] = True  # => only the OVEN is ready so far -- dough is NOT
        cond.notify_all()  # => wakes the waiter EARLY, before the real predicate holds


log: list[str] = []
waiter = threading.Thread(target=baker_waits_for_both, args=(log,))
waiter.start()
time.sleep(0.05)  # => gives the waiter time to reach cond.wait() before the controller signals
controller_signals_progress()  # => a legitimate partial-progress notify -- NOT the full predicate
waiter.join(timeout=1.0)
print(log)
assert log == ["baking: oven=True dough=False"]  # => confirms the baker started with the dough NOT ready
print("kata OK (bug reproduced)")
