"""Example 61: Denormalize vs. Normalize Tradeoff."""  # => co-09: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => enables the explicit MongoClient[dict[str, Any]] type parameter below (DD-39, pyright --strict)

from pymongo import MongoClient  # => co-09: pymongo, the official typed Python driver

Document = dict[str, Any]  # => co-09: pymongo's own convention for "a MongoDB document" -- every field's own type varies per-document


def seed_denormalized(client: MongoClient[Document]) -> None:  # => co-09: ONE document holds the author AND every one of its 5 posts, embedded
    """Model an author-with-posts relation DENORMALIZED -- all posts embedded in one document."""  # => documents the contract
    collection = client["nosqldb"]["authors_denormalized"]  # => co-09: a dedicated collection for the denormalized shape
    collection.delete_many({})  # => resets state -- this example is fully self-contained
    collection.insert_one(
        {  # => co-09: the WHOLE one-to-many relation in ONE document
            "name": "Ada",  # => the "one" side of the relation, embedded directly
            "posts": [{"title": f"Post {i}"} for i in range(5)],  # => co-09: 5 posts, embedded directly -- no separate collection
        }
    )  # => closes the insert_one() call -- author AND posts land as a SINGLE document


def seed_normalized(client: MongoClient[Document]) -> str:  # => co-09: TWO collections, posts referencing the author by id
    """Model the SAME relation NORMALIZED -- posts in a separate collection, referencing the author."""  # => documents contract
    authors = client["nosqldb"]["authors_normalized"]  # => the "one" side, in its own collection
    posts = client["nosqldb"]["posts_normalized"]  # => the "many" side, in a SEPARATE collection
    authors.delete_many({})  # => resets state -- this example is fully self-contained
    posts.delete_many({})  # => resets the posts side too
    author_id = authors.insert_one({"name": "Ada"}).inserted_id  # => co-09: no posts embedded here at all
    for i in range(5):  # => co-09: 5 posts, each referencing author_id -- no enforced foreign key in MongoDB
        posts.insert_one({"author_id": author_id, "title": f"Post {i}"})  # => a SEPARATE insert, SEPARATE document, per post
    return str(author_id)  # => hand back the author id the normalized read needs


def read_denormalized_query_count(client: MongoClient[Document]) -> int:  # => co-09: counts round trips for the embedded shape's common read
    """Read an author with all posts, denormalized -- count the queries this costs."""  # => documents the contract
    collection = client["nosqldb"]["authors_denormalized"]  # => selects the collection seed_denormalized just populated
    doc = collection.find_one({"name": "Ada"})  # => co-09: query 1 -- author AND all 5 posts arrive together
    assert doc is not None and len(doc["posts"]) == 5  # => co-09: all 5 posts present, from ONE query
    return 1  # => co-09: exactly ONE query answered the WHOLE relation


def read_normalized_query_count(client: MongoClient[Document], author_id: str) -> int:  # => co-09: counts round trips for the referenced shape's common read
    """Read an author with all posts, normalized -- count the queries this costs, including the N+1 pattern."""  # => documents contract
    from bson import ObjectId  # => co-09: converts the string id back to a real ObjectId for the query below

    authors = client["nosqldb"]["authors_normalized"]  # => the "one" side collection
    posts = client["nosqldb"]["posts_normalized"]  # => the "many" side collection
    query_count = 0  # => tracks every round trip this function issues
    author = authors.find_one({"_id": ObjectId(author_id)})  # => co-09: query 1 -- fetches the author ALONE, no posts yet
    query_count += 1  # => counts this first query
    assert author is not None  # => confirms the author genuinely exists
    post_list = list(posts.find({"author_id": ObjectId(author_id)}))  # => co-09: query 2 -- a SEPARATE round trip for the posts
    query_count += 1  # => counts this second query
    assert len(post_list) == 5  # => co-09: all 5 posts found, but it cost a SECOND round trip
    return query_count  # => hand back the total query count for this read


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = MongoClient("mongodb://localhost:27017")  # => connects to a local MongoDB instance
    seed_denormalized(client)  # => sets up the embedded-shape fixture
    author_id = seed_normalized(client)  # => sets up the referenced-shape fixture

    denormalized_queries = read_denormalized_query_count(client)  # => co-09: the embedded shape's common-read query count
    normalized_queries = read_normalized_query_count(client, author_id)  # => co-09: the referenced shape's common-read query count

    print(f"Denormalized (embedded) read: {denormalized_queries} query")  # => Output: Denormalized (embedded) read: 1 query
    print(f"Normalized (referenced) read: {normalized_queries} queries")  # => Output: Normalized (referenced) read: 2 queries
    assert denormalized_queries == 1  # => co-09: the denormalized shape needs exactly ONE query for the common read
    assert normalized_queries == 2  # => co-09: the referenced shape needs an author query PLUS a separate posts query (N+1 pattern, here N=1 relation, so 1+1=2)
    print("Denormalized shape needs ONE query; the referenced shape needs an author query PLUS a separate posts query")  # => Output line
    client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
