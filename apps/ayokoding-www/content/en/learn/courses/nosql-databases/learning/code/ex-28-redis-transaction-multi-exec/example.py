"""Example 28: Redis Transaction MULTI/EXEC."""  # => co-27: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import redis  # => co-27: redis-py, the official typed Python client for Valkey/Redis


def transfer_atomically(client: redis.Redis, from_key: str, to_key: str, amount: int) -> None:  # => co-27: moves amount atomically
    """Move amount from from_key to to_key inside a MULTI/EXEC transaction."""  # => documents the contract
    pipe = client.pipeline(transaction=True)  # => co-27: transaction=True queues commands, then EXECs them as one unit
    pipe.multi()  # => co-27: MULTI -- starts queuing, no command below runs yet
    pipe.decrby(from_key, amount)  # => co-27: QUEUED, not yet applied -- decrements the source balance
    pipe.incrby(to_key, amount)  # => co-27: QUEUED, not yet applied -- increments the destination balance
    pipe.execute()  # => co-27: EXEC -- both queued commands apply together, back-to-back, no other client's write interleaves
    # => note (co-27): EXEC does NOT roll back on a runtime error inside the block -- a queued command
    # => that fails at execution time (e.g. wrong type) still lets the OTHER queued commands apply;
    # => MULTI/EXEC buys ATOMIC APPLICATION of a queued batch, not ACID-style all-or-nothing rollback


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = redis.Redis(host="localhost", port=6379, db=0)  # => connects to a local Valkey/Redis instance
    client.delete("wallet:alice", "wallet:bob")  # => resets state -- this example is fully self-contained
    client.set("wallet:alice", 100)  # => alice starts with 100
    client.set("wallet:bob", 50)  # => bob starts with 50

    transfer_atomically(client, "wallet:alice", "wallet:bob", 30)  # => co-27: moves 30 from alice to bob atomically

    alice_raw = client.get("wallet:alice")  # => reads alice's post-transfer balance, as bytes | None
    bob_raw = client.get("wallet:bob")  # => reads bob's post-transfer balance, as bytes | None
    assert alice_raw is not None and bob_raw is not None  # => both keys were SET above -- narrows away the None case for int()
    alice_balance = int(alice_raw)  # => decodes the raw bytes reply into a plain int
    bob_balance = int(bob_raw)  # => decodes the raw bytes reply into a plain int
    assert alice_balance == 70  # => co-27: 100 - 30 == 70, the debit applied
    assert bob_balance == 80  # => co-27: 50 + 30 == 80, the credit applied -- BOTH updates landed together
    print(f"After MULTI/EXEC transfer: alice={alice_balance} bob={bob_balance}")  # => Output: After MULTI/EXEC transfer: alice=70 bob=80
    client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
