"""Example 29: Redis WATCH Optimistic Lock."""  # => co-27: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import redis  # => co-27: redis-py, the official typed Python client
from redis.exceptions import WatchError  # => co-27: redis-py raises WatchError when a watched key changed


def try_transfer_with_watch(client: redis.Redis, key: str, amount: int, tamper: bool) -> bool:  # => co-27: returns True if the tx committed
    """Attempt a WATCH-guarded transfer; optionally tamper the watched key mid-flight to force an abort."""  # => documents contract
    with client.pipeline() as pipe:  # => a fresh pipeline per attempt, matching real optimistic-locking retry loops
        pipe.watch(key)  # => co-27: WATCH -- flags this key; if it changes before EXEC, the transaction aborts
        if tamper:  # => simulates ANOTHER client concurrently modifying the watched key between WATCH and EXEC
            client.incr(key)  # => co-27: a concurrent write on the SAME key this pipeline is watching
        pipe.multi()  # => co-27: MULTI -- starts queuing, still inside the SAME watched pipeline
        pipe.decrby(key, amount)  # => co-27: QUEUED -- will only apply if the watched key stayed untouched
        try:  # => catches ONLY the WatchError EXEC raises on a detected race, nothing else
            pipe.execute()  # => co-27: EXEC -- aborts (raises WatchError) if the watched key changed since WATCH
            return True  # => the transaction committed -- the watched key was untouched by anyone else
        except WatchError:  # => co-27: redis-py surfaces the server's nil EXEC reply as this exception
            return False  # => the transaction aborted -- optimistic concurrency correctly detected the race


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = redis.Redis(host="localhost", port=6379, db=0)  # => connects to a local Valkey/Redis instance
    client.set("inventory:sku-42", 100)  # => resets state -- this example is fully self-contained

    committed_clean = try_transfer_with_watch(client, "inventory:sku-42", 10, tamper=False)  # => co-27: no interference -- should commit
    assert committed_clean is True  # => co-27: WATCH saw no change, so EXEC applied the queued DECRBY
    print(f"No interference: transaction committed = {committed_clean}")  # => Output: No interference: transaction committed = True

    committed_tampered = try_transfer_with_watch(client, "inventory:sku-42", 10, tamper=True)  # => co-27: tampers the SAME key mid-flight
    assert committed_tampered is False  # => co-27: WATCH caught the concurrent INCR, EXEC returned nil, redis-py raised WatchError
    print(f"Concurrent write during WATCH: transaction committed = {committed_tampered}")  # => Output: Concurrent write during WATCH: transaction committed = False
    client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
