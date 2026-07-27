"""Example 13: MongoDB createIndex()."""  # => co-17,co-18: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => enables the explicit MongoClient[dict[str, Any]] type parameter below (DD-39, pyright --strict)

from pymongo import MongoClient  # => co-18: pymongo, the official typed Python driver

Document = dict[str, Any]  # => co-18: pymongo's own convention for "a MongoDB document" -- every field's own type varies per-document


def seed_large_collection(client: MongoClient[Document]) -> None:  # => enough documents that an index measurably matters
    """Reset and seed 2000 documents, only one matching a later equality filter."""  # => documents the contract
    collection = client["nosqldb"]["users_indexed"]  # => co-17: a dedicated collection for this index demonstration
    collection.delete_many({})  # => resets state -- this example is fully self-contained
    collection.insert_many(  # => co-18: 2000 documents, enough that a COLLSCAN is genuinely more expensive
        [{"email": f"user{i}@example.com", "active": i % 3 == 0} for i in range(2000)]  # => generates 2000 distinct emails, deterministically
    )  # => only ONE document will match email == "user1500@example.com" below


def explain_before_and_after_index(client: MongoClient[Document]) -> tuple[str, str]:  # => returns the winning stage, before/after
    """Run the same equality query before and after an index, reading explain()'s winning stage."""  # => documents contract
    collection = client["nosqldb"]["users_indexed"]  # => selects the collection seed_large_collection just populated
    query = {"email": "user1500@example.com"}  # => a single-document equality match, the worst case for a full scan

    before = collection.find(query).explain()  # => co-17: explain() WITHOUT an index -- must check every document
    before_stage = before["queryPlanner"]["winningPlan"]["stage"]  # => co-17: the top-level plan stage MongoDB chose
    assert before_stage == "COLLSCAN"  # => co-17: no usable index exists yet -- a full collection scan

    collection.create_index("email")  # => co-17: creates a single-field ascending index on "email"
    after = collection.find(query).explain()  # => the SAME query, re-explained now that an index exists
    after_stage = after["queryPlanner"]["winningPlan"]["inputStage"]["stage"]  # => co-17: the leaf scan stage under the fetch
    assert after_stage == "IXSCAN"  # => co-17: the planner now walks the index instead of every document

    return before_stage, after_stage  # => hand both stage names back for the caller to print


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = MongoClient("mongodb://localhost:27017")  # => connects to a local MongoDB instance
    seed_large_collection(client)  # => sets up the 2000-document fixture
    before_stage, after_stage = explain_before_and_after_index(client)  # => runs the before/after explain() comparison
    print(f"Before index: {before_stage} | After index: {after_stage}")  # => Output: Before index: COLLSCAN | After index: IXSCAN
    client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
