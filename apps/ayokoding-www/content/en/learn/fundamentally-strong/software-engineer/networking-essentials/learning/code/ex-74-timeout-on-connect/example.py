"""Example 74: A Socket Timeout on connect() to an Unreachable Host."""

import socket  # => stdlib sockets -- connect()'s own timeout parameter is the whole demonstration
import time  # => wall-clock timing is what proves the timeout was actually honored

# 192.0.2.0/24 is TEST-NET-1 (RFC 5737): reserved for documentation, deliberately
# NOT routed on the real internet -- connect() here can never succeed OR be refused,
# it can only time out (co-10).
UNREACHABLE_HOST = "192.0.2.1"  # => co-01: guaranteed non-routed, unlike Example 59's real hosts  # fmt: skip
PORT = 80  # => co-05: the port doesn't matter here -- the HOST itself is unreachable
TIMEOUT_SECONDS = 2.0  # => the exact upper bound this example's assertion below checks against  # fmt: skip

start = time.perf_counter()  # => a clock reading taken right before the doomed connect() attempt  # fmt: skip
try:  # => wrapped because a TimeoutError (or, on some networks, an OSError) is EXPECTED here
    conn = socket.create_connection((UNREACHABLE_HOST, PORT), timeout=TIMEOUT_SECONDS)
    # => blocks for AT MOST timeout seconds, then raises
    conn.close()  # => reached only if the connection unexpectedly succeeded
    outcome = "connected (unexpected on this reserved, non-routed network)"
except TimeoutError:  # => co-10: no SYN-ACK and no RST ever arrived -- silence, not rejection  # fmt: skip
    outcome = "TimeoutError raised, as expected"
except OSError as err:  # => some networks respond with an ICMP unreachable instead of silence  # fmt: skip
    outcome = f"OSError raised instead: {err}"
elapsed = time.perf_counter() - start  # => convert to a real, measured elapsed duration

print(f"outcome: {outcome}")  # => expect "TimeoutError raised, as expected" on a real network  # fmt: skip
print(f"elapsed: {elapsed:.2f}s (timeout was set to {TIMEOUT_SECONDS}s)")  # => bounded, not endless  # fmt: skip

assert elapsed < TIMEOUT_SECONDS + 1.0  # => confirms the call didn't hang well past the timeout  # fmt: skip
print("ex-74 OK")  # => confirms the timeout was honored, bounding an otherwise-endless wait  # fmt: skip
