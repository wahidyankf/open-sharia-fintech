# pyright: strict
"""Example 74: Retry with FULL JITTER. (co-38)

Plain exponential backoff clusters retries: when many clients fail at once,
they all retry at base*2^n together, producing synchronized retry storms. FULL
JITTER replaces the capped delay with a UNIFORM random value in [0, capped
delay]: sleep = random(0, min(cap, base*2^attempt)). Clients de-synchronize.
Source: AWS "Exponential Backoff and Jitter" (Marc Brooker, 2015). A FIXED
SEED makes the output deterministic for this example.
"""

import random  # => stdlib: uniform random for full jitter
from dataclasses import dataclass  # => a small typed record for one client's schedule


def full_jitter_delay(attempt: int, base_seconds: float = 1.0, cap_seconds: float = 32.0, rng: random.Random | None = None) -> float:
    # => co-38: Full Jitter: sleep = random(0, min(cap, base*2^(attempt-1)))
    bound = min(cap_seconds, base_seconds * (2 ** (attempt - 1)))  # => the capped exponential ceiling
    engine = rng if rng is not None else random.Random(0)  # => a seeded RNG for deterministic output
    return engine.uniform(0, bound)  # => a uniform random value in [0, bound]


@dataclass  # => co-38: one client's full-jitter retry schedule
class ClientSchedule:
    client: str  # => the client label
    delays: list[float]  # => this client's de-synchronized delay sequence


def schedule_for(client: str, attempts: int, seed: int) -> ClientSchedule:  # => one client's seeded schedule
    rng = random.Random(seed)  # => co-38: a distinct seed per client -> distinct (de-synchronized) delays
    delays = [full_jitter_delay(n, rng=rng) for n in range(1, attempts + 1)]  # => jittered delays
    return ClientSchedule(client=client, delays=delays)  # => the schedule


# Two clients failing at the SAME time get DIFFERENT retry schedules -> no synchronized storm.
client_a = schedule_for("A", attempts=4, seed=1)  # => co-38: seed 1
client_b = schedule_for("B", attempts=4, seed=2)  # => co-38: seed 2
print(f"client A delays: {[round(d, 2) for d in client_a.delays]}")  # => Output: jittered, distinct
print(f"client B delays: {[round(d, 2) for d in client_b.delays]}")  # => Output: jittered, distinct

desynchronized = client_a.delays != client_b.delays  # => co-38: the two clients retry at different times
within_bounds = all(0 <= d <= min(32, 1 * 2 ** (n - 1)) for n, d in enumerate(client_a.delays, 1))  # => co-38: each in [0, bound]
print(f"clients de-synchronized: {desynchronized}")  # => Output: True
print(f"client A delays within [0, bound]: {within_bounds}")  # => Output: True

assert desynchronized  # => co-38: full jitter de-synchronizes clients
assert within_bounds  # => co-38: every delay is in [0, min(cap, base*2^(attempt-1))]
