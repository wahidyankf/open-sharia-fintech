"""Example 12a: MongoDB Embedded -- one-to-many modeled as a nested array."""  # => co-09,co-18: purpose, doubling as __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => enables the explicit MongoClient[dict[str, Any]] type parameter below (DD-39, pyright --strict)

from pymongo import MongoClient  # => co-18: pymongo, the official typed Python driver

Document = dict[str, Any]  # => co-18: pymongo's own convention for "a MongoDB document" -- every field's own type varies per-document


def seed_embedded(client: MongoClient[Document]) -> None:  # => one author document, comments embedded INSIDE it
    """Model author-with-comments as ONE document, comments nested as an array field."""  # => documents the contract
    collection = client["nosqldb"]["articles_embedded"]  # => co-09: a dedicated collection for the embedded shape
    collection.delete_many({})  # => resets state -- this example is fully self-contained
    collection.insert_one(
        {  # => co-09: the WHOLE one-to-many relation lives in a SINGLE document
            "title": "NoSQL 101",  # => the "one" side's own field -- no separate row/table needed for it
            "comments": [  # => co-09: an embedded array -- every comment travels WITH its parent article
                {"author": "Bob", "text": "Great intro!"},  # => comment 1, nested directly inside the parent document
                {"author": "Carol", "text": "More examples please"},  # => comment 2, nested alongside comment 1
            ],  # => closes the embedded array -- both comments are now part of the ONE document written below
        }
    )  # => a SINGLE insert_one call persists the article AND both comments together, atomically


def read_article_with_comments(client: MongoClient[Document]) -> dict[str, object]:  # => a SINGLE fetch returns article + comments
    """Fetch the article and its comments with exactly one round trip."""  # => documents the contract
    collection = client["nosqldb"]["articles_embedded"]  # => selects the collection seed_embedded just populated
    doc = collection.find_one({"title": "NoSQL 101"})  # => co-09: ONE query -- comments arrive already attached
    assert doc is not None  # => the seeded document genuinely exists
    return doc  # => hand the full document, comments included, back to the caller


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = MongoClient("mongodb://localhost:27017")  # => connects to a local MongoDB instance
    seed_embedded(client)  # => sets up the embedded-shape fixture
    doc = read_article_with_comments(client)  # => runs the single-query read
    comments = doc["comments"]  # => the array field pulled along for free with the parent read
    assert isinstance(comments, list) and len(comments) == 2  # => co-09: both comments arrived in the SAME read
    print(f"Embedded read: 1 query, {len(comments)} comments attached")  # => Output: Embedded read: 1 query, 2 comments attached
    client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
