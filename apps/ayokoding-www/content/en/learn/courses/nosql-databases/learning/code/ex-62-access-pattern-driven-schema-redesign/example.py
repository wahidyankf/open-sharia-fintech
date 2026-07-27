"""Example 62: Access-Pattern-Driven Schema Redesign."""  # => co-08: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => enables the explicit MongoClient[dict[str, Any]] type parameter below (DD-39, pyright --strict)

from bson import ObjectId  # => co-08: MongoDB's own generated primary-key type -- every insert_one().inserted_id is one of these
from pymongo import MongoClient  # => co-08: pymongo, the official typed Python driver

Document = dict[str, Any]  # => co-08: pymongo's own convention for "a MongoDB document" -- every field's own type varies per-document

# The two NAMED access patterns this redesign must serve, stated up front, in plain English (co-08):
ACCESS_PATTERN_1 = "fetch a product with its current average rating"  # => the FIRST dominant read
ACCESS_PATTERN_2 = "fetch the 3 most recent reviews for a product"  # => the SECOND dominant read


def seed_naive_schema(client: MongoClient[Document]) -> None:  # => co-08: the STARTING point -- a schema that does NOT serve either pattern in one query
    """Seed a naive schema: a product document, reviews in a fully separate collection with no aggregate."""  # => documents contract
    products = client["nosqldb"]["products_naive"]  # => co-08: the naive product collection -- no rating aggregate stored
    reviews = client["nosqldb"]["reviews_naive"]  # => co-08: reviews live entirely separately, unordered relative to the product
    products.delete_many({})  # => resets state -- this example is fully self-contained
    reviews.delete_many({})  # => resets the reviews side too
    product_id = products.insert_one({"sku": "sku-7", "name": "Desk Lamp"}).inserted_id  # => co-08: NO rating field at all -- pattern 1 would need a live aggregation
    for i, rating in enumerate([5, 3, 4, 5, 2]):  # => co-08: 5 reviews, inserted in order, but NOT clustered/indexed for "most recent"
        reviews.insert_one({"product_id": product_id, "rating": rating, "review_id": i, "text": f"review {i}"})  # => co-08: SEPARATE document per review, no aggregate anywhere


def naive_pattern_1_cost(client: MongoClient[Document], product_id: ObjectId) -> int:  # => co-08: counts queries the NAIVE schema needs for pattern 1
    """Answer pattern 1 (product + avg rating) against the NAIVE schema -- requires a live aggregation."""  # => documents the contract
    reviews = client["nosqldb"]["reviews_naive"]  # => the naive reviews collection
    pipeline = [{"$match": {"product_id": product_id}}, {"$group": {"_id": None, "avg": {"$avg": "$rating"}}}]  # => a LIVE aggregation, every time
    list(reviews.aggregate(pipeline))  # => co-08: this is a SECOND, more expensive query, EVERY time pattern 1 runs
    return 2  # => co-08: 1 query for the product + 1 aggregation query for the rating -- NOT a single fetch


def redesign_schema(client: MongoClient[Document]) -> ObjectId:  # => co-08: derives a NEW shape FROM the two named access patterns
    """Redesign the schema so BOTH access patterns are served by a single query each."""  # => documents the contract
    products = client["nosqldb"]["products_redesigned"]  # => co-08: the redesigned product collection
    products.delete_many({})  # => resets state -- this example is fully self-contained
    product_id = products.insert_one(
        {  # => co-08: the shape DERIVED from the two access patterns, not from a generic entity diagram
            "sku": "sku-7",  # => the product's own stable identifier
            "name": "Desk Lamp",  # => the product's own display name
            "avg_rating": 3.8,  # => co-08: a MAINTAINED running average -- satisfies pattern 1 with the product's own document
            "recent_reviews": [  # => co-08: the 3 MOST RECENT reviews, embedded directly -- satisfies pattern 2 with no separate query
                {"review_id": 4, "rating": 2, "text": "review 4"},  # => the MOST recent of the 3 embedded reviews
                {"review_id": 3, "rating": 5, "text": "review 3"},  # => the second-most-recent embedded review
                {"review_id": 2, "rating": 4, "text": "review 2"},  # => the third-most-recent embedded review -- oldest of the 3 kept
            ],  # => closes the recent_reviews list -- exactly 3 entries, no separate collection needed
        }
    ).inserted_id  # => co-08: the single insert_one() call's own generated ObjectId
    return product_id  # => hand back the id both redesigned-pattern reads below will use


def redesigned_pattern_1_cost(client: MongoClient[Document], product_id: ObjectId) -> tuple[int, float]:  # => co-08: (query count, avg_rating) for the REDESIGNED schema
    """Answer pattern 1 against the REDESIGNED schema -- a single document read."""  # => documents the contract
    products = client["nosqldb"]["products_redesigned"]  # => the redesigned product collection
    doc = products.find_one({"_id": product_id})  # => co-08: ONE query -- avg_rating is ALREADY on the document
    assert doc is not None  # => confirms the redesigned document genuinely exists
    return 1, doc["avg_rating"]  # => co-08: exactly ONE query answered pattern 1


def redesigned_pattern_2_cost(client: MongoClient[Document], product_id: ObjectId) -> tuple[int, int]:  # => co-08: (query count, review count) for the REDESIGNED schema
    """Answer pattern 2 against the REDESIGNED schema -- a single document read."""  # => documents the contract
    products = client["nosqldb"]["products_redesigned"]  # => the redesigned product collection
    doc = products.find_one({"_id": product_id})  # => co-08: ONE query -- recent_reviews is ALREADY on the document
    assert doc is not None  # => confirms the redesigned document genuinely exists
    return 1, len(doc["recent_reviews"])  # => co-08: exactly ONE query answered pattern 2


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client: MongoClient[Document] = MongoClient("mongodb://localhost:27017")  # => connects to a local MongoDB instance
    print(f"Pattern 1: {ACCESS_PATTERN_1}")  # => Output line
    print(f"Pattern 2: {ACCESS_PATTERN_2}")  # => Output line

    seed_naive_schema(client)  # => sets up the STARTING, naive fixture
    products_naive = client["nosqldb"]["products_naive"]  # => selects the naive product collection to find its id
    naive_product = products_naive.find_one({"sku": "sku-7"})  # => reads the naive product back, to extract its own generated id
    assert naive_product is not None  # => confirms the naive fixture genuinely seeded a matching document
    naive_product_id = naive_product["_id"]  # => the naive product's own id, for the cost check below
    naive_cost = naive_pattern_1_cost(client, naive_product_id)  # => co-08: measures the NAIVE schema's own cost for pattern 1
    assert naive_cost == 2  # => co-08: the naive schema needs 2 queries -- NOT a single fetch
    print(f"Naive schema, pattern 1 cost: {naive_cost} queries")  # => Output: Naive schema, pattern 1 cost: 2 queries

    redesigned_id = redesign_schema(client)  # => co-08: derives the new shape FROM the two access patterns
    p1_queries, avg_rating = redesigned_pattern_1_cost(client, redesigned_id)  # => co-08: measures the REDESIGNED cost for pattern 1
    p2_queries, review_count = redesigned_pattern_2_cost(client, redesigned_id)  # => co-08: measures the REDESIGNED cost for pattern 2
    assert p1_queries == 1 and avg_rating == 3.8  # => co-08: pattern 1 now costs exactly ONE query
    assert p2_queries == 1 and review_count == 3  # => co-08: pattern 2 now costs exactly ONE query
    print(f"Redesigned schema, pattern 1 cost: {p1_queries} query (avg_rating={avg_rating})")  # => Output: Redesigned schema, pattern 1 cost: 1 query (avg_rating=3.8)
    print(f"Redesigned schema, pattern 2 cost: {p2_queries} query ({review_count} recent reviews)")  # => Output: Redesigned schema, pattern 2 cost: 1 query (3 recent reviews)
    print("Both named access patterns now served by a single query each, after the redesign")  # => Output line
    client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
