"""Example 12b: MongoDB Referenced -- one-to-many modeled as two collections."""  # => co-09,co-18: purpose, doubling as __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => enables the explicit MongoClient[dict[str, Any]] type parameter below (DD-39, pyright --strict)

from pymongo import MongoClient  # => co-18: pymongo, the official typed Python driver

Document = dict[str, Any]  # => co-18: pymongo's own convention for "a MongoDB document" -- every field's own type varies per-document


def seed_referenced(client: MongoClient[Document]) -> object:  # => two collections, comments hold a FOREIGN reference back
    """Model author-with-comments as TWO collections, joined by a stored article_id."""  # => documents the contract
    articles = client["nosqldb"]["articles_referenced"]  # => co-09: the "one" side lives in its own collection
    comments = client["nosqldb"]["comments_referenced"]  # => co-09: the "many" side lives in a SEPARATE collection
    articles.delete_many({})  # => resets state -- this example is fully self-contained
    comments.delete_many({})  # => resets the comments side too
    article_id = articles.insert_one({"title": "NoSQL 101"}).inserted_id  # => co-09: no comments embedded here at all
    comments.insert_many(
        [  # => co-09: each comment stores article_id -- MongoDB has NO enforced foreign key
            {"article_id": article_id, "author": "Bob", "text": "Great intro!"},  # => comment 1, referencing the article by id, not nested inside it
            {"article_id": article_id, "author": "Carol", "text": "More examples please"},  # => comment 2, same foreign-key-style reference
        ]
    )  # => TWO separate insert calls persist the article and its comments across DIFFERENT collections
    return article_id  # => hand back the id the caller needs for the second query below


def read_article_with_comments(client: MongoClient[Document], article_id: object) -> tuple[Document, list[Document]]:  # => TWO queries
    """Fetch the article, then a SEPARATE query for its comments -- two round trips, not one."""  # => documents the contract
    articles = client["nosqldb"]["articles_referenced"]  # => selects the "one" side collection
    comments = client["nosqldb"]["comments_referenced"]  # => selects the "many" side collection
    article = articles.find_one({"_id": article_id})  # => co-09: query 1 -- the article alone, no comments attached
    assert article is not None  # => the seeded article genuinely exists
    comment_list = list(comments.find({"article_id": article_id}))  # => co-09: query 2 -- a SEPARATE round trip for comments
    return article, comment_list  # => the caller must combine both results itself


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = MongoClient("mongodb://localhost:27017")  # => connects to a local MongoDB instance
    article_id = seed_referenced(client)  # => sets up the referenced-shape fixture
    _article, comment_list = read_article_with_comments(client, article_id)  # => runs the TWO-query read
    assert len(comment_list) == 2  # => co-09: both comments found, but it cost a second round trip to get them
    print(f"Referenced read: 2 queries, {len(comment_list)} comments joined manually")  # => Output: Referenced read: 2 queries, 2 comments joined manually
    client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
