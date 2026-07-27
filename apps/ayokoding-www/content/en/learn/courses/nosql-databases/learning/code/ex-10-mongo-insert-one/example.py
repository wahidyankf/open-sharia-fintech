"""Example 10: MongoDB insert_one."""  # => co-18: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => enables the explicit MongoClient[dict[str, Any]] type parameter below (DD-39, pyright --strict)

from bson import ObjectId  # => co-18: BSON's own 12-byte identifier type, what a generated _id actually is
from pymongo import MongoClient  # => co-18: pymongo, the official typed Python driver for MongoDB

Document = dict[str, Any]  # => co-18: pymongo's own convention for "a MongoDB document" -- every field's own type varies per-document


def insert_and_verify(client: MongoClient[Document]) -> ObjectId:  # => inserts one document, returns its generated _id
    """Insert one document with no explicit _id and confirm MongoDB generated one."""  # => documents the contract
    db = client["nosqldb"]  # => co-18: selects (and lazily creates, on first write) the "nosqldb" database
    collection = db["articles"]  # => co-18: a collection is schema-less -- no CREATE TABLE step exists
    result = collection.insert_one({"title": "NoSQL 101", "author": "Ada", "views": 0})  # => co-18: no _id field supplied
    assert isinstance(result.inserted_id, ObjectId)  # => co-18: MongoDB auto-generates a unique ObjectId when none is given
    stored = collection.find_one({"_id": result.inserted_id})  # => reads the document back by its generated _id
    assert stored is not None  # => the document genuinely exists under that _id
    assert stored["title"] == "NoSQL 101"  # => confirms the stored fields match exactly what was inserted
    return result.inserted_id  # => hand back the generated id for the caller to print


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = MongoClient("mongodb://localhost:27017")  # => connects to a local MongoDB instance
    new_id = insert_and_verify(client)  # => runs the verified insert above
    print(f"Inserted document with generated _id: {new_id}")  # => Output: Inserted document with generated _id: <a 24-hex-char ObjectId, e.g. 66f1a2b3c4d5e6f7a8b9c0d1>
    client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
