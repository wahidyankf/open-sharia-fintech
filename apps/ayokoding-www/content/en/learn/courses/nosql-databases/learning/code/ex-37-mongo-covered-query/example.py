"""Example 37: MongoDB Covered Query."""  # => co-17: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => enables the explicit MongoClient[dict[str, Any]] type parameter below (DD-39, pyright --strict)

from pymongo import MongoClient  # => co-17: pymongo, the official typed Python driver

Document = dict[str, Any]  # => co-17: pymongo's own convention for "a MongoDB document" -- every field's own type varies per-document


def seed_users(client: MongoClient[Document]) -> None:  # => documents with an extra field NOT touched by the covered query below
    """Reset and seed 500 users, each with an indexed email and an unrelated bio field."""  # => documents the contract
    collection = client["nosqldb"]["users_covered"]  # => co-17: a dedicated collection for this covered-query demonstration
    collection.delete_many({})  # => resets state -- this example is fully self-contained
    collection.insert_many(
        [  # => co-17: 500 documents, "bio" exists but is NEVER referenced by the query or projection below
            {"email": f"user{i}@example.com", "active": i % 2 == 0, "bio": f"bio text for user {i}" * 3}  # => bio is deliberately large and UNINDEXED
            for i in range(500)  # => generates all 500 documents deterministically
        ]
    )  # => the covered query below must answer using ONLY email + active, never touching bio


def explain_covered_query(client: MongoClient[Document]) -> int:  # => co-17: returns totalDocsExamined, expected to be exactly 0
    """Create an index over exactly the queried and projected fields, then confirm the query is COVERED."""  # => documents contract
    collection = client["nosqldb"]["users_covered"]  # => selects the collection seed_users just populated
    collection.create_index([("email", 1), ("active", 1)])  # => co-17: an index over BOTH the filter field and the projected field
    explanation = collection.find(  # => co-17: query the SAME two fields the index covers
        {"email": "user250@example.com"},  # => filters on email -- part of the index
        {"active": 1, "_id": 0},  # => projects ONLY active, also part of the index, and explicitly drops _id
    ).explain()  # => co-17: explain() reveals whether the server needed to fetch the full document at all
    total_docs_examined = explanation["executionStats"]["totalDocsExamined"]  # => co-17: 0 means the index ALONE answered the query
    return total_docs_examined  # => hand the raw count back for the caller to assert and print


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = MongoClient("mongodb://localhost:27017")  # => connects to a local MongoDB instance
    seed_users(client)  # => sets up the 500-document fixture
    total_docs_examined = explain_covered_query(client)  # => runs the covered-query verification
    assert total_docs_examined == 0  # => co-17: a COVERED query -- the index alone answered it, the full document was NEVER fetched
    print(f"Covered query totalDocsExamined: {total_docs_examined} (index alone answered the query)")  # => Output: Covered query totalDocsExamined: 0 (index alone answered the query)
    client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
