"""Example 68: Schema-on-Read Migration."""  # => co-18: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => enables the explicit MongoClient[dict[str, Any]] type parameter below (DD-39, pyright --strict)

from pymongo import MongoClient  # => co-18: pymongo, the official typed Python driver

Document = dict[str, Any]  # => co-18: pymongo's own convention for "a MongoDB document" -- every field's own type varies per-document


def seed_pre_migration_documents(client: MongoClient[Document]) -> None:  # => co-18: the OLD shape, before any field was ever added
    """Seed 3 documents in the OLD shape, before a new field was ever conceived."""  # => documents the contract
    collection = client["nosqldb"]["users_migration"]  # => co-18: no schema declared for this collection, ever
    collection.delete_many({})  # => resets state -- this example is fully self-contained
    collection.insert_many(
        [  # => co-18: 3 documents, the OLD shape -- no "newsletter_opt_in" field exists yet
            {"name": "Bob", "email": "bob@example.com"},  # => the OLD shape -- only name and email, no opt-in field
            {"name": "Carol", "email": "carol@example.com"},  # => the OLD shape, stays untouched through the whole example
            {"name": "Dave", "email": "dave@example.com"},  # => the OLD shape, stays untouched through the whole example
        ]
    )  # => closes the insert_many() call -- 3 documents, none carrying the new field


def add_field_to_some_documents(client: MongoClient[Document]) -> None:  # => co-18: the "MIGRATION" -- but really just NEW writes, no ALTER TABLE
    """Add newsletter_opt_in to ONE new document and ONE existing document -- the rest stay untouched."""  # => documents contract
    collection = client["nosqldb"]["users_migration"]  # => selects the collection seed_pre_migration_documents just populated
    collection.insert_one({"name": "Eve", "email": "eve@example.com", "newsletter_opt_in": True})  # => co-18: a BRAND NEW document, with the NEW field from the start
    collection.update_one({"name": "Bob"}, {"$set": {"newsletter_opt_in": False}})  # => co-18: ONE existing document explicitly updated with the new field
    # => Carol and Dave are DELIBERATELY left untouched -- no migration script ran across the whole
    # => collection; the new field simply does not exist on their documents


def read_with_default(client: MongoClient[Document]) -> dict[str, bool]:  # => co-18: the READER's own responsibility to default a missing field
    """Read every user's newsletter_opt_in, defaulting to False when the field is entirely missing."""  # => documents contract
    collection = client["nosqldb"]["users_migration"]  # => selects the collection add_field_to_some_documents just modified
    results: dict[str, bool] = {}  # => accumulates name -> resolved opt-in status
    for doc in collection.find({}):  # => co-18: iterates OLD-shape (no field), NEWLY-updated (field=False), and NEW (field=True) documents together
        results[doc["name"]] = doc.get("newsletter_opt_in", False)  # => co-18: the READER supplies the default -- KeyError would fire on doc["newsletter_opt_in"] for Carol/Dave
    return results  # => hand the resolved per-user opt-in map back to the caller


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = MongoClient("mongodb://localhost:27017")  # => connects to a local MongoDB instance
    seed_pre_migration_documents(client)  # => sets up the pre-migration, 3-document fixture
    add_field_to_some_documents(client)  # => co-18: adds the new field to SOME, not ALL, documents -- no migration script
    results = read_with_default(client)  # => runs the schema-tolerant, defaulting read

    assert results == {"Bob": False, "Carol": False, "Dave": False, "Eve": True}  # => co-18: Bob and Eve have the field explicitly, Carol/Dave get the DEFAULT
    for name in sorted(results):  # => prints the resolved opt-in status for every user, sorted for deterministic output
        print(f"{name}: newsletter_opt_in={results[name]}")  # => Output line, one per user
    print("Old documents (Carol, Dave) and new documents (Bob, Eve) both read correctly -- zero migration step ever ran")  # => Output line
    client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
