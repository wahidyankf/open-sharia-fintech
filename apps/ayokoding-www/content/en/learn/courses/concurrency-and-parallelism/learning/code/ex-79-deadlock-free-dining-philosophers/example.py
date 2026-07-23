"""Example 79: Dining Philosophers -- Deadlock-Free, via a Global Fork-Acquisition Order."""

import threading  # => co-16, co-18: the CLASSIC deadlock scenario, fixed with ex-30's SAME lock-ordering trick
import time  # => bounds how long each philosopher "eats" and "thinks"

PHILOSOPHER_COUNT = 5  # => the traditional five philosophers, five forks, arranged in a circle
MEALS_PER_PHILOSOPHER = 3  # => how many times EACH philosopher must successfully eat


def philosopher(philosopher_id: int, forks: list[threading.Lock], meals_eaten: list[int], meals_target: int) -> None:
    left_fork = philosopher_id  # => left_fork: this philosopher's LEFT fork index, by seating position
    right_fork = (philosopher_id + 1) % PHILOSOPHER_COUNT  # => right_fork: the NEXT seat's fork, wrapping around

    first_fork = min(left_fork, right_fork)  # => first_fork: ALWAYS the LOWER-numbered fork, regardless of side
    second_fork = max(left_fork, right_fork)  # => second_fork: ALWAYS the HIGHER-numbered fork -- the fix (co-18)
    # => this GLOBAL order (lowest fork first, for EVERY philosopher) is exactly ex-30's fix, applied here:
    # => it breaks the circular-wait condition that would otherwise deadlock all five philosophers at once

    for _ in range(meals_target):  # => this philosopher eats exactly `meals_target` times, then stops
        with forks[first_fork]:  # => acquires the LOWER-numbered fork first -- NEVER the higher one first
            with forks[second_fork]:  # => acquires the HIGHER-numbered fork second -- consistent for EVERYONE
                meals_eaten[philosopher_id] += 1  # => this philosopher successfully "ate" one meal
                time.sleep(0.001)  # => simulates the brief time spent actually eating, while holding both forks
        time.sleep(0.001)  # => simulates "thinking" -- time spent NOT holding any forks, between meals


def run_dinner() -> list[int]:
    forks = [threading.Lock() for _ in range(PHILOSOPHER_COUNT)]  # => forks: one Lock per fork, shared by neighbors
    meals_eaten = [0] * PHILOSOPHER_COUNT  # => meals_eaten[i]: how many times philosopher i has successfully eaten
    philosophers = [
        threading.Thread(target=philosopher, args=(i, forks, meals_eaten, MEALS_PER_PHILOSOPHER))
        for i in range(PHILOSOPHER_COUNT)  # => one thread per philosopher, all sharing the SAME `forks` list
    ]  # => philosophers: exactly PHILOSOPHER_COUNT Thread objects, not yet started
    for p in philosophers:  # => starts every philosopher
        p.start()  # => all five immediately begin competing for forks, using the SAME global order
    for p in philosophers:  # => waits for every philosopher to finish eating MEALS_PER_PHILOSOPHER times
        p.join(timeout=5)  # => a generous timeout -- if this ever times out, a deadlock genuinely occurred
    return meals_eaten  # => how many meals each philosopher ACTUALLY completed


if __name__ == "__main__":  # => module entry point
    meals_eaten = run_dinner()  # => drives the whole dinner to completion (or reveals a hang via the timeout)
    print(f"meals_eaten={meals_eaten}")  # => Output: meals_eaten=[3, 3, 3, 3, 3]

    # => The classic dining-philosophers deadlock happens when EVERY philosopher picks up their LEFT
    # => fork first: all five now hold one fork each and wait forever for their right neighbor's fork --
    # => a five-way circular wait (co-16), the same shape as ex-29's two-thread deadlock, just bigger.
    # => Imposing a GLOBAL fork-acquisition order -- always the LOWER-numbered fork first, for EVERY
    # => philosopher, regardless of which is "left" or "right" -- makes that circular wait structurally
    # => impossible (co-18): at least one philosopher's "first" fork is always free for SOMEONE to start.
    assert meals_eaten == [MEALS_PER_PHILOSOPHER] * PHILOSOPHER_COUNT  # => confirms EVERY philosopher ate, fully
    print("ex-79 OK")  # => Output: ex-79 OK
