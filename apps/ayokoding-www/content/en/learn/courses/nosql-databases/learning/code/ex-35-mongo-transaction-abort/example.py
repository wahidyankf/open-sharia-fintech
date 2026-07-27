"""Example 35: MongoDB Transaction Abort."""  # => co-27: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => enables the explicit MongoClient[dict[str, Any]] type parameter below (DD-39, pyright --strict)

from pymongo import MongoClient  # => co-27: pymongo, the official typed Python driver

Document = dict[str, Any]  # => co-27: pymongo's own convention for "a MongoDB document" -- every field's own type varies per-document


class DeliberateFailure(Exception):  # => co-27: a custom exception standing in for a real mid-transaction business-rule error
    """Raised deliberately mid-transaction to force an abort."""  # => documents intent, no runtime output


def seed_accounts(client: MongoClient[Document]) -> None:  # => two documents, one write staged then deliberately aborted
    """Reset and seed two account documents."""  # => documents the contract, no runtime output
    accounts = client["nosqldb"]["accounts_abort"]  # => co-27: a SEPARATE collection so this example does not collide with Example 34
    accounts.delete_many({})  # => resets state -- this example is fully self-contained
    accounts.insert_many([{"_id": "carol", "balance": 200}, {"_id": "dave", "balance": 10}])  # => starting balances


def transfer_that_fails_midway(client: MongoClient[Document], amount: int) -> bool:  # => co-27: returns True if the abort happened as expected
    """Stage a debit, force an error before the credit, and confirm the whole transaction rolled back."""  # => documents contract
    accounts = client["nosqldb"]["accounts_abort"]  # => selects the collection seed_accounts just populated
    try:  # => catches ONLY the deliberate business-rule exception, to prove the transaction rolled back cleanly
        with client.start_session() as session, session.start_transaction():  # => co-27: session scopes; start_transaction begins it -- one combined `with`
            accounts.update_one({"_id": "carol"}, {"$inc": {"balance": -amount}}, session=session)  # => co-27: staged debit, NOT yet visible outside
            raise DeliberateFailure("business rule violated mid-transfer")  # => co-27: forces an error BEFORE the matching credit runs
            # => the line below is intentionally unreachable -- the raise above always fires first
            accounts.update_one({"_id": "dave"}, {"$inc": {"balance": amount}}, session=session)  # pragma: no cover
    except DeliberateFailure:  # => co-27: the `with session.start_transaction()` block exits via exception -> implicit ABORT
        return True  # => co-27: the staged debit was rolled back entirely -- pymongo aborts on an uncaught exception in the block
    return False  # => unreachable in this example -- included only so the function's return type is total


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = MongoClient("mongodb://localhost:27017")  # => connects to a local MongoDB replica-set instance
    seed_accounts(client)  # => sets up the two-account fixture
    aborted = transfer_that_fails_midway(client, 50)  # => co-27: runs the deliberately-failing transaction
    assert aborted is True  # => confirms the DeliberateFailure path was taken

    accounts = client["nosqldb"]["accounts_abort"]  # => selects the collection to verify NO partial write landed
    carol = accounts.find_one({"_id": "carol"})  # => reads carol's balance AFTER the aborted transaction
    dave = accounts.find_one({"_id": "dave"})  # => reads dave's balance AFTER the aborted transaction
    assert carol is not None and carol["balance"] == 200  # => co-27: UNCHANGED -- the staged debit was rolled back, not partially applied
    assert dave is not None and dave["balance"] == 10  # => co-27: UNCHANGED -- the credit never even ran
    print(f"After aborted transaction: carol={carol['balance']} dave={dave['balance']} (both unchanged)")  # => Output: After aborted transaction: carol=200 dave=10 (both unchanged)
    client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
