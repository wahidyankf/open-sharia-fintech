"""Example 63: Secondary Index vs. Denormalization."""  # => co-17,co-09: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => enables the explicit MongoClient[dict[str, Any]] type parameter below (DD-39, pyright --strict)

from pymongo import MongoClient  # => co-17: pymongo, the official typed Python driver

Document = dict[str, Any]  # => co-17: pymongo's own convention for "a MongoDB document" -- every field's own type varies per-document

# The access pattern neither collection's PRIMARY key alone can serve: "find all orders for a given author name."


def seed_orders_and_authors(client: MongoClient[Document]) -> None:  # => co-09: a fixture BOTH approaches below start from
    """Seed authors and orders referencing them by id -- neither collection's own key answers the target pattern."""  # => documents contract
    authors = client["nosqldb"]["authors_63"]  # => the "one" side
    orders = client["nosqldb"]["orders_63"]  # => the "many" side, keyed by order_id, NOT by author name
    authors.delete_many({})  # => resets state -- this example is fully self-contained
    orders.delete_many({})  # => resets the orders side too
    author_id = authors.insert_one({"name": "Ada"}).inserted_id  # => co-09: the author's own id
    for i in range(3):  # => co-17: 3 orders for Ada, referenced by author_id, NOT by name
        orders.insert_one({"order_id": i, "author_id": author_id, "amount": (i + 1) * 10})


def approach_secondary_index(client: MongoClient[Document]) -> list[int]:  # => co-17: a SECONDARY INDEX on the join key, then a client-side 2-query join
    """Approach A: create a secondary index on author_id, then query orders by it -- 2 collections stay separate."""  # => documents contract
    authors = client["nosqldb"]["authors_63"]  # => selects the authors collection
    orders = client["nosqldb"]["orders_63"]  # => selects the orders collection
    orders.create_index("author_id")  # => co-17: a secondary index on the join key -- SPEEDS the lookup, does NOT eliminate the second query
    author = authors.find_one({"name": "Ada"})  # => query 1 -- finds Ada's own id
    assert author is not None  # => confirms Ada genuinely exists
    matched_orders = list(orders.find({"author_id": author["_id"]}))  # => co-17: query 2, now INDEX-SERVED rather than a collection scan
    return sorted(order["amount"] for order in matched_orders)  # => hand back the amounts, sorted for a deterministic assertion


def approach_denormalization(client: MongoClient[Document]) -> list[int]:  # => co-09: DUPLICATES the author name directly onto each order
    """Approach B: denormalize the author name directly onto each order document -- ONE collection, no join at all."""  # => documents contract
    orders_denorm = client["nosqldb"]["orders_63_denorm"]  # => co-09: a SEPARATE collection, deliberately duplicating author_name
    orders_denorm.delete_many({})  # => resets state -- this example is fully self-contained
    for i in range(3):  # => co-09: the SAME 3 orders, but with author_name duplicated directly onto EACH one
        orders_denorm.insert_one({"order_id": i, "author_name": "Ada", "amount": (i + 1) * 10})  # => co-09: no join needed -- the name is RIGHT THERE
    matched_orders = list(orders_denorm.find({"author_name": "Ada"}))  # => co-09: ONE query, no join, no second collection touched
    return sorted(order["amount"] for order in matched_orders)  # => hand back the amounts, sorted for a deterministic assertion


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = MongoClient("mongodb://localhost:27017")  # => connects to a local MongoDB instance
    seed_orders_and_authors(client)  # => sets up the shared fixture both approaches read from

    index_result = approach_secondary_index(client)  # => co-17: Approach A -- secondary index, still 2 queries
    denorm_result = approach_denormalization(client)  # => co-09: Approach B -- denormalized, 1 query, no join

    assert index_result == denorm_result == [10, 20, 30]  # => co-17,co-09: BOTH approaches return the IDENTICAL result set
    print(f"Secondary-index approach result: {index_result} (2 queries: author lookup, then indexed order lookup)")  # => Output: Secondary-index approach result: [10, 20, 30] (2 queries: author lookup, then indexed order lookup)
    print(f"Denormalized approach result:    {denorm_result} (1 query: author_name duplicated onto every order)")  # => Output: Denormalized approach result:    [10, 20, 30] (1 query: author_name duplicated onto every order)
    print("Identical results, different cost profiles: index=2 queries+extra index storage; denormalized=1 query+write-side duplication risk")  # => Output line
    # => co-17,co-09: the secondary index keeps a SINGLE source of truth for the author's name (update it
    # => once, every order's lookup sees the change) at the cost of a second query; denormalization
    # => collapses to one query at the cost of updating EVERY order if the author's name ever changes


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
