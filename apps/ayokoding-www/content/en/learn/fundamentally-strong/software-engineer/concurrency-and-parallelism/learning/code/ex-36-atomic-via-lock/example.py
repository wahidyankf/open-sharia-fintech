"""Example 36: Any Read-Modify-Write Needs a Lock, Not Just `+= 1`."""

import threading  # => generalizes ex-08/ex-11's lesson (co-10, co-11) beyond plain increment
import time  # => widens the race window with the same `sleep(0)` technique as ex-08

DEPOSITS_A = [2] * 500  # => thread A makes 500 deposits of $2 each -- a VARYING-amount RMW, not +=1
DEPOSITS_B = [3] * 500  # => thread B makes 500 deposits of $3 each -- a DIFFERENT amount than A


def deposit_no_lock(balance: list[int], amounts: list[int]) -> None:  # => the UNSYNCHRONIZED version
    for amount in amounts:  # => applies each deposit amount in turn
        current = balance[0]  # => READ the current balance -- step 1 of the read-modify-write
        time.sleep(0)  # => yields here -- widens the window for another thread's own read-modify-write
        balance[0] = current + amount  # => WRITE BACK current + amount -- step 3, using the OLD `current`


def deposit_with_lock(balance: list[int], amounts: list[int], lock: threading.Lock) -> None:  # => the FIX
    for amount in amounts:  # => applies each deposit amount in turn
        with lock:  # => the ENTIRE read-modify-write sequence below runs as one atomic critical section
            current = balance[0]  # => READ -- no other thread can interleave here while the lock is held
            time.sleep(0)  # => still yields -- proving the LOCK prevents interleaving, not luck
            balance[0] = current + amount  # => WRITE BACK -- still inside the SAME critical section


if __name__ == "__main__":  # => module entry point
    expected_total = sum(DEPOSITS_A) + sum(DEPOSITS_B)  # => expected_total: the mathematically correct sum

    unsynced_balance = [0]  # => a fresh balance for the UNSYNCHRONIZED run
    t1 = threading.Thread(target=deposit_no_lock, args=(unsynced_balance, DEPOSITS_A))
    t2 = threading.Thread(target=deposit_no_lock, args=(unsynced_balance, DEPOSITS_B))
    # => t1, t2: two threads that BOTH call the unsynchronized version against the SAME balance
    t1.start()  # => starts thread A's unsynchronized deposits
    t2.start()  # => starts thread B's unsynchronized deposits -- races with A on the SAME balance
    t1.join()  # => waits for thread A to finish all 500 of its deposits
    t2.join()  # => waits for thread B to finish all 500 of its deposits

    locked_balance = [0]  # => a fresh balance for the LOCK-PROTECTED run
    guard = threading.Lock()  # => the ONE lock both threads share for this run
    t3 = threading.Thread(target=deposit_with_lock, args=(locked_balance, DEPOSITS_A, guard))
    t4 = threading.Thread(target=deposit_with_lock, args=(locked_balance, DEPOSITS_B, guard))
    # => t3, t4: the SAME shape as t1/t2, but sharing `guard` -- the only difference that matters
    t3.start()  # => starts thread A's lock-protected deposits
    t4.start()  # => starts thread B's lock-protected deposits -- still races for the LOCK, not the balance
    t3.join()  # => waits for thread A to finish
    t4.join()  # => waits for thread B to finish

    print(f"expected={expected_total} unsynced={unsynced_balance[0]} locked={locked_balance[0]}")
    # => Output: expected=2500 unsynced=<less than 2500> locked=2500

    # => The lesson generalizes beyond `x += 1`: ANY read-modify-write -- adding a variable amount,
    # => appending to a list, incrementing a dict value -- loses updates under concurrent access
    # => unless the ENTIRE read-modify-write sequence is protected by the SAME lock, every time.
    assert unsynced_balance[0] < expected_total  # => confirms the unsynchronized version lost deposits
    assert locked_balance[0] == expected_total  # => confirms the lock-protected version is EXACT
    print("ex-36 OK")  # => Output: ex-36 OK
