"""Example 34: MongoDB Multi-Document Transaction."""  # => co-27: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => enables the explicit MongoClient[dict[str, Any]] type parameter below (DD-39, pyright --strict)

from pymongo import MongoClient  # => co-27: pymongo, the official typed Python driver

Document = dict[str, Any]  # => co-27: pymongo's own convention for "a MongoDB document" -- every field's own type varies per-document


def seed_accounts(client: MongoClient[Document]) -> None:  # => two documents, moved between atomically below
    """Reset and seed two account documents."""  # => documents the contract, no runtime output
    accounts = client["nosqldb"]["accounts"]  # => co-27: a dedicated collection for this transaction demonstration
    accounts.delete_many({})  # => resets state -- this example is fully self-contained
    accounts.insert_many([{"_id": "alice", "balance": 100}, {"_id": "bob", "balance": 50}])  # => starting balances


def transfer_in_transaction(client: MongoClient[Document], amount: int) -> None:  # => co-27: a SESSION-scoped, ACID-style transaction
    """Move amount from alice to bob inside a session-scoped multi-document transaction."""  # => documents contract
    accounts = client["nosqldb"]["accounts"]  # => selects the collection seed_accounts just populated
    with client.start_session() as session, session.start_transaction():  # => co-27: session scopes; start_transaction begins it -- one combined `with`
        accounts.update_one({"_id": "alice"}, {"$inc": {"balance": -amount}}, session=session)  # => co-27: staged debit, tied to this session
        accounts.update_one({"_id": "bob"}, {"$inc": {"balance": amount}}, session=session)  # => co-27: staged credit, tied to this SAME session
        # => co-27: leaving the `with` block cleanly triggers an implicit COMMIT -- BOTH updates
        # => become visible to other clients atomically, in one instant, or NEITHER does


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = MongoClient("mongodb://localhost:27017")  # => connects to a local MongoDB replica-set instance (transactions require one)
    seed_accounts(client)  # => sets up the two-account fixture
    transfer_in_transaction(client, 30)  # => co-27: runs the session-scoped atomic transfer

    accounts = client["nosqldb"]["accounts"]  # => selects the collection to verify the committed result
    alice = accounts.find_one({"_id": "alice"})  # => reads alice's post-transaction balance
    bob = accounts.find_one({"_id": "bob"})  # => reads bob's post-transaction balance
    assert alice is not None and alice["balance"] == 70  # => co-27: 100 - 30 == 70, the debit committed
    assert bob is not None and bob["balance"] == 80  # => co-27: 50 + 30 == 80, the credit committed -- BOTH atomically
    print(f"After transaction commit: alice={alice['balance']} bob={bob['balance']}")  # => Output: After transaction commit: alice=70 bob=80
    client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
