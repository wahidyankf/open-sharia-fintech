"""Example 37: A Data Race and a Logic Race Fail in DIFFERENT Ways."""

import threading  # => contrasts co-08 (data race) against co-09 (a synchronized-but-still-wrong race)
import time  # => the `sleep(0)` interleaving technique proven reliable since ex-08

WITHDRAWALS = 2000  # => how many times each thread tries to decrement during the data-race demo
# => a smaller count is used directly for the logic-race demo below (WITHDRAWALS itself, unmodified)


def data_race_decrement(balance: list[int], times: int) -> None:  # => NO lock anywhere in this function
    for _ in range(times):  # => repeats the unsynchronized read-modify-write `times` times
        current = balance[0]  # => READ -- step 1, with no lock protecting it at all
        time.sleep(0)  # => widens the window -- proven to force a lost update, per ex-08/ex-11
        balance[0] = current - 1  # => WRITE BACK -- step 3, using the now-STALE `current`


def logic_race_withdraw(balance: list[int], amount: int, lock: threading.Lock, successes: list[int], checked_barrier: threading.Barrier) -> None:
    # => checked_barrier: a Barrier(2) that makes the check-then-act GAP deterministic for the demo
    with lock:  # => the READ is individually protected...
        can_afford = balance[0] >= amount  # => can_afford: True if the balance covers this withdrawal
    checked_barrier.wait()  # => forces BOTH threads to finish their check before EITHER proceeds to act
    if can_afford:  # => acts on a decision that is GUARANTEED stale for one of the two threads
        with lock:  # => the WRITE is ALSO individually protected...
            balance[0] -= amount  # => ...but the CHECK-THEN-ACT pair, as a whole, is NOT atomic
            successes[0] += 1  # => counts a "successful" withdrawal (even if it overdrew the account)


if __name__ == "__main__":  # => module entry point
    data_race_balance = [0]  # => starts at 0; two threads each decrement it WITHDRAWALS times
    t1 = threading.Thread(target=data_race_decrement, args=(data_race_balance, WITHDRAWALS))
    t2 = threading.Thread(target=data_race_decrement, args=(data_race_balance, WITHDRAWALS))
    t1.start()  # => starts the first unsynchronized decrementer
    t2.start()  # => starts the second -- races with t1 on the exact same list cell
    t1.join()  # => waits for both threads to finish their WITHDRAWALS decrements each
    t2.join()  # => the expected final value is -2 * WITHDRAWALS if nothing were lost
    expected_data_race = -2 * WITHDRAWALS  # => expected_data_race: the mathematically correct total
    print(f"data_race: expected={expected_data_race} actual={data_race_balance[0]}")
    # => Output: data_race: expected=-4000 actual=<a number CLOSER TO ZERO than -4000> (lost updates)

    logic_race_balance = [WITHDRAWALS]  # => starts with EXACTLY enough for ONE thread to withdraw it all
    guard = threading.Lock()  # => protects each individual read and each individual write
    successes = [0]  # => counts how many withdrawals were allowed to "succeed"
    checked_barrier = threading.Barrier(2)  # => rendezvous point AFTER both checks, BEFORE either act
    t3 = threading.Thread(target=logic_race_withdraw, args=(logic_race_balance, WITHDRAWALS, guard, successes, checked_barrier))
    # => t3: the first withdrawer -- shares logic_race_balance, guard, and checked_barrier with t4
    t4 = threading.Thread(target=logic_race_withdraw, args=(logic_race_balance, WITHDRAWALS, guard, successes, checked_barrier))
    # => t4: the second withdrawer -- an IDENTICAL request, timed to collide via the shared barrier
    t3.start()  # => starts the first withdrawer -- checks, waits at the barrier, then acts
    t4.start()  # => starts the second -- MUST also reach the barrier before either one can act
    t3.join()  # => waits for both withdrawal attempts to finish
    t4.join()  # => the barrier GUARANTEES both checks completed before either write happened
    print(f"logic_race: final_balance={logic_race_balance[0]} successes={successes[0]}")
    # => Output: logic_race: final_balance=-2000 successes=2 (BOTH thought they could afford it)

    # => The data race fails by LOSING updates -- the total drifts TOWARD zero, unpredictably, because
    # => each individual statement is unsynchronized. The logic race fails DIFFERENTLY: every individual
    # => statement IS correctly locked, yet the balance still goes NEGATIVE, because the CHECK and the
    # => ACT are two separate critical sections with a gap between them (a TOCTOU bug, co-09). The
    # => `Barrier` here makes the gap DETERMINISTIC for teaching purposes; in production code the same
    # => bug appears sporadically, from ordinary thread scheduling, with no barrier needed to trigger it.
    # => Fixing a data race needs a lock around the whole read-modify-write; fixing a logic race needs
    # => the lock to span the ENTIRE check-then-act sequence, not just its individual parts.
    assert data_race_balance[0] > expected_data_race  # => confirms updates were lost (closer to zero, not more negative)
    assert logic_race_balance[0] < 0  # => confirms the "safely locked" version still overdrew the account
    print("ex-37 OK")  # => Output: ex-37 OK
