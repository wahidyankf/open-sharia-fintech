"""Example 14: MongoDB Schema-on-Read."""  # => co-18: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => enables the explicit MongoClient[dict[str, Any]] type parameter below (DD-39, pyright --strict)

from pymongo import MongoClient  # => co-18: pymongo, the official typed Python driver

Document = dict[str, Any]  # => co-18: pymongo's own convention for "a MongoDB document" -- every field's own type varies per-document


def seed_mixed_shapes(client: MongoClient[Document]) -> None:  # => two documents in ONE collection, deliberately different shapes
    """Insert an old-shape and a new-shape document into the SAME collection."""  # => documents the contract
    collection = client["nosqldb"]["users_mixed"]  # => co-18: no schema is declared for this collection, ever
    collection.delete_many({})  # => resets state -- this example is fully self-contained
    collection.insert_one({"name": "Bob", "email": "bob@example.com"})  # => co-18: the OLD shape -- no "phone" field
    collection.insert_one({"name": "Carol", "email": "carol@example.com", "phone": "+62-812-000"})  # => co-18: the NEW shape
    # => MongoDB accepted BOTH inserts with no error -- no ALTER TABLE, no migration ran between them


def read_with_default(client: MongoClient[Document]) -> list[str]:  # => the reader, not the store, must handle the missing field
    """Read every user, defaulting a missing phone field -- the reader's own responsibility."""  # => documents contract
    collection = client["nosqldb"]["users_mixed"]  # => selects the collection seed_mixed_shapes just populated
    results: list[str] = []  # => accumulates one formatted line per document
    for doc in collection.find({}):  # => co-18: iterates BOTH the old-shape and new-shape documents, same collection
        phone = doc.get("phone", "(no phone on file)")  # => co-18: the READER checks presence and supplies a default
        # => a MISSING key access (doc["phone"]) would raise KeyError on Bob's old-shape document instead
        results.append(f"{doc['name']}: {phone}")  # => builds one readable line per user
    return results  # => hand the formatted lines back to the caller


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = MongoClient("mongodb://localhost:27017")  # => connects to a local MongoDB instance
    seed_mixed_shapes(client)  # => sets up the two-different-shapes fixture
    lines = read_with_default(client)  # => runs the schema-tolerant read
    assert lines == ["Bob: (no phone on file)", "Carol: +62-812-000"]  # => co-18: both shapes read correctly, no migration
    print("\n".join(lines))  # => Output: Bob: (no phone on file)\nCarol: +62-812-000
    client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
