"""Example 31: MongoDB Aggregation $match + $group."""  # => co-19: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => enables the explicit MongoClient[dict[str, Any]] type parameter below (DD-39, pyright --strict)

from pymongo import MongoClient  # => co-19: pymongo, the official typed Python driver

Document = dict[str, Any]  # => co-19: pymongo's own convention for "a MongoDB document" -- every field's own type varies per-document


def seed_orders(client: MongoClient[Document]) -> None:  # => a deterministic fixture across 3 categories, one order excluded by status
    """Reset and seed 5 orders across 3 categories, one cancelled (excluded by the pipeline's $match)."""  # => documents contract
    collection = client["nosqldb"]["orders"]  # => co-19: no schema declared for this collection
    collection.delete_many({})  # => resets state -- this example is fully self-contained
    collection.insert_many(
        [  # => co-19: 5 orders, one "cancelled" -- the pipeline below must exclude it
            {"category": "books", "amount": 20, "status": "paid"},  # => books order 1, paid -- counted below
            {"category": "books", "amount": 15, "status": "paid"},  # => books order 2, paid -- counted below
            {"category": "electronics", "amount": 200, "status": "paid"},  # => electronics order 1, paid -- counted below
            {"category": "electronics", "amount": 50, "status": "cancelled"},  # => excluded by $match below
            {"category": "toys", "amount": 30, "status": "paid"},  # => toys' only order, paid -- counted below
        ]
    )  # => 5 orders total, but only 4 are "paid" -- the $match stage must drop exactly 1


def total_paid_per_category(client: MongoClient[Document]) -> dict[str, int]:  # => co-19: server-side aggregate, one round trip
    """Run a $match + $group pipeline computing a per-category paid total."""  # => documents the contract
    collection = client["nosqldb"]["orders"]  # => selects the collection seed_orders just populated
    pipeline = [  # => co-19: a staged pipeline -- each stage's output feeds the next stage's input
        {"$match": {"status": "paid"}},  # => co-19: stage 1 -- keeps only paid orders, drops the cancelled one
        {"$group": {"_id": "$category", "total": {"$sum": "$amount"}}},  # => co-19: stage 2 -- sums amount PER distinct category
    ]  # => 2 stages, run server-side in ONE round trip -- no client-side filtering or summing needed
    results = list(collection.aggregate(pipeline))  # => co-19: ONE round trip runs the WHOLE pipeline server-side
    return {doc["_id"]: doc["total"] for doc in results}  # => reshapes the cursor into a plain category->total dict


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = MongoClient("mongodb://localhost:27017")  # => connects to a local MongoDB instance
    seed_orders(client)  # => sets up the 5-order, 3-category fixture
    totals = total_paid_per_category(client)  # => runs the $match + $group aggregation
    assert totals == {"books": 35, "electronics": 200, "toys": 30}  # => co-19: cancelled electronics order correctly excluded
    for category in sorted(totals):  # => co-19: prints the aggregate result, sorted for deterministic output
        print(f"{category}: {totals[category]}")  # => Output line, one per category
    client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
