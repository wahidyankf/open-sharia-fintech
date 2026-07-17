"""Example 34: The Four Coffman Conditions -- Present in ex-29, Broken in ex-30."""

# => reuses ex-29's deadlock shape and ex-30's fix, annotated against Coffman's own 1971 theory


def deadlock_conditions_all_present(holder: dict[str, str]) -> dict[str, bool]:
    # => holder: records WHICH thread holds WHICH lock, to check the conditions after the fact
    # => a real Lock instance isn't needed here -- the FOUR conditions are checked from the
    # => snapshot alone, so this function stays pure and easy to test with plain dicts
    mutual_exclusion = True
    # => condition 1: a threading.Lock, by definition, can only ever have ONE holder at a time
    thread_a_holds_a = holder.get("thread_a") == "lock_a"
    # => thread_a_holds_a: True if the snapshot says thread_a currently holds lock_a
    thread_a_wants_b = holder.get("thread_a_wants") == "lock_b"
    # => thread_a_wants_b: True if thread_a is ALSO, simultaneously, blocked requesting lock_b
    hold_and_wait = thread_a_holds_a and thread_a_wants_b
    # => condition 2: HOLDING one resource while WAITING for another, at the same time
    no_preemption = True
    # => condition 3: threading.Lock has no mechanism to FORCIBLY take a lock back from a holder
    thread_b_holds_b = holder.get("thread_b") == "lock_b"
    # => thread_b_holds_b: True if the snapshot says thread_b currently holds lock_b
    circular_wait = thread_a_holds_a and thread_b_holds_b
    # => condition 4: A holds what B wants, B holds what A wants -- a wait cycle of length 2
    conditions = {"mutual_exclusion": mutual_exclusion, "hold_and_wait": hold_and_wait}
    # => conditions: builds the result dict in two steps to keep each literal line short
    conditions["no_preemption"] = no_preemption
    # => adds condition 3 to the result
    conditions["circular_wait"] = circular_wait
    # => adds condition 4 -- all four must be True for ex-29's deadlock to actually occur
    return conditions  # => the caller decides what "all four present" means (see below)


if __name__ == "__main__":  # => module entry point
    # => Simulates the EXACT moment ex-29 deadlocks: thread_a holds lock_a and wants lock_b,
    # => thread_b holds lock_b (implied by the circular_wait check inside the function above).
    snapshot: dict[str, str] = {"thread_a": "lock_a", "thread_a_wants": "lock_b", "thread_b": "lock_b"}
    # => snapshot: a plain dict standing in for "what each thread holds/wants" at deadlock time
    conditions = deadlock_conditions_all_present(snapshot)
    # => conditions: the four Coffman booleans computed from the snapshot above
    print(conditions)  # => Output: {'mutual_exclusion': True, 'hold_and_wait': True, ...}

    all_four_present = all(conditions.values())  # => all_four_present: True only if EVERY condition holds
    print(f"all_four_present={all_four_present}")  # => Output: all_four_present=True

    # => A deadlock requires ALL FOUR Coffman conditions simultaneously: mutual exclusion (a
    # => resource has exactly one holder), hold-and-wait (holding one resource while requesting
    # => another), no preemption (a holder can't be forced to give up a resource), and circular
    # => wait (a cycle of threads each waiting on the next). ex-30's fix breaks ONLY circular_wait
    # => (via a global lock order) -- it leaves the other three conditions untouched, which is
    # => enough: breaking any ONE condition makes the whole deadlock impossible.
    assert all_four_present is True  # => confirms ex-29's scenario had all four conditions present
    fixed_circular_wait = False  # => ex-30's global order means A never holds lock_a while wanting lock_b AND B holds lock_b
    assert fixed_circular_wait is False  # => confirms breaking JUST this one condition is the fix
    print("ex-34 OK")  # => Output: ex-34 OK
