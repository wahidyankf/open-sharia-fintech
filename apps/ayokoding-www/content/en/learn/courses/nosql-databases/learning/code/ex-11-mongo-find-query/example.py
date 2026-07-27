"""Example 11: MongoDB find() Query."""  # => co-18: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => enables the explicit MongoClient[dict[str, Any]] type parameter below (DD-39, pyright --strict)

from pymongo import MongoClient  # => co-18: pymongo, the official typed Python driver

Document = dict[str, Any]  # => co-18: pymongo's own convention for "a MongoDB document" -- every field's own type varies per-document


def seed_articles(client: MongoClient[Document]) -> None:  # => resets and reseeds a small, deterministic fixture
    """Reset the articles collection and seed 3 documents, 2 matching a later filter."""  # => documents the contract
    collection = client["nosqldb"]["articles"]  # => co-18: collections need no schema declared up front
    collection.delete_many({})  # => resets state -- this example is fully self-contained
    collection.insert_many(
        [  # => co-18: insert_many writes multiple documents in one round trip
            {"title": "NoSQL 101", "author": "Ada", "views": 340, "published": True},  # => matches the filter below (author Ada, published)
            {"title": "CAP Theorem Explained", "author": "Ada", "views": 512, "published": True},  # => matches too, and has MORE views
            {"title": "Draft: Vector Clocks", "author": "Ada", "views": 0, "published": False},  # => same author, but published: False -- must be excluded
        ]
    )  # => 3 documents seeded, only 2 have published: True


def find_published_by_ada(client: MongoClient[Document]) -> list[str]:  # => returns titles matching the filter, sorted by views
    """Return titles of Ada's published articles, most-viewed first."""  # => documents the contract
    collection = client["nosqldb"]["articles"]  # => selects the same collection seed_articles just populated
    cursor = collection.find(  # => co-18: find() takes a filter document -- an implicit AND across its keys
        {"author": "Ada", "published": True},  # => matches only documents where BOTH conditions hold
        {"title": 1, "_id": 0},  # => a PROJECTION -- return only title, and explicitly suppress _id
    ).sort("views", -1)  # => -1 means descending -- highest view count first
    return [doc["title"] for doc in cursor]  # => materializes the cursor into a plain list of titles


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = MongoClient("mongodb://localhost:27017")  # => connects to a local MongoDB instance
    seed_articles(client)  # => sets up the deterministic 3-document fixture
    titles = find_published_by_ada(client)  # => runs the filtered, sorted, projected query
    assert titles == ["CAP Theorem Explained", "NoSQL 101"]  # => co-18: only the 2 published docs, higher views first
    print(f"Published articles by Ada, most-viewed first: {titles}")  # => Output: Published articles by Ada, most-viewed first: ['CAP Theorem Explained', 'NoSQL 101']
    client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
