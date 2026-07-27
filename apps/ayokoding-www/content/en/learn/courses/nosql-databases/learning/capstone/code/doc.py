"""Capstone Step 2: doc.py -- a product catalog shaped by two named access patterns (co-08, co-17, co-19).

Builds directly on Example 78's own preview shape: fields chosen FROM the access patterns,
not the other way around, with a compound index that makes both patterns index-served,
verified via `.explain()` rather than assumed. This module adds `update_stock`, a realistic
write path pattern 1's own field (`stock_level`) exists to support.
"""

from __future__ import annotations

from typing import Any  # => pymongo's own documents are untyped dicts -- Any is the honest, pymongo-recommended document type

from pymongo import MongoClient  # => the official typed Python driver (Apache-2.0, co-28)

Document = dict[str, Any]  # => pymongo's own convention for "a MongoDB document" -- every field's own type varies per-document

# The capstone's two named access patterns (co-08) -- every field in seed_products exists to serve one of these.
ACCESS_PATTERN_1 = "fetch a product with its current stock level"
ACCESS_PATTERN_2 = "fetch every product in a given category, cheapest first"
COLLECTION_NAME = "capstone_products"


def seed_products(client: MongoClient[Document]) -> None:
    """Seed a small catalog, with indexes chosen to serve BOTH named access patterns."""
    collection = client["nosqldb"][COLLECTION_NAME]
    collection.delete_many({})  # => resets state -- this script is fully self-contained
    collection.insert_many(
        [
            {"sku": "sku-1", "category": "electronics", "price": 29.99, "stock_level": 12},
            {"sku": "sku-2", "category": "electronics", "price": 9.99, "stock_level": 0},
            {"sku": "sku-3", "category": "books", "price": 14.50, "stock_level": 40},
            {"sku": "sku-4", "category": "books", "price": 6.75, "stock_level": 5},
        ]
    )
    collection.create_index("sku")  # => serves pattern 1: a single-document lookup by sku
    collection.create_index([("category", 1), ("price", 1)])  # => serves pattern 2: category-then-price, pre-sorted


def fetch_product_with_stock(client: MongoClient[Document], sku: str) -> tuple[bool, int]:
    """Answer pattern 1: fetch a product with its stock level, via an index-served single-document read."""
    collection = client["nosqldb"][COLLECTION_NAME]
    explanation: Document = collection.find({"sku": sku}).explain()  # => confirms the query is genuinely INDEX-served
    index_served: bool = explanation["queryPlanner"]["winningPlan"]["stage"] == "FETCH"  # => FETCH-from-IXSCAN means the sku index was used
    doc = collection.find_one({"sku": sku})
    assert doc is not None
    return index_served, doc["stock_level"]


def fetch_category_cheapest_first(client: MongoClient[Document], category: str) -> tuple[bool, list[float]]:
    """Answer pattern 2: fetch a category's products cheapest-first, via an index-served, pre-sorted read."""
    collection = client["nosqldb"][COLLECTION_NAME]
    cursor = collection.find({"category": category}).sort("price", 1)  # => the compound index ALREADY sorts by price
    explanation: Document = collection.find({"category": category}).sort("price", 1).explain()  # => confirms index usage
    index_served: bool = "IXSCAN" in str(explanation["queryPlanner"]["winningPlan"])  # => a simple, honest presence check
    prices: list[float] = [doc["price"] for doc in cursor]  # => extracts prices in RETURN order -- already sorted by the index
    return index_served, prices


def update_stock(client: MongoClient[Document], sku: str, new_stock_level: int) -> None:
    """A realistic write: adjust a product's stock level -- the exact field pattern 1 reads back."""
    collection = client["nosqldb"][COLLECTION_NAME]
    collection.update_one({"sku": sku}, {"$set": {"stock_level": new_stock_level}})


def main() -> None:
    """Seed the catalog, answer both access patterns, verify each is index-served, and print a report."""
    client: MongoClient[Document] = MongoClient("mongodb://localhost:27017")
    print(f"Pattern 1: {ACCESS_PATTERN_1}")
    print(f"Pattern 2: {ACCESS_PATTERN_2}")

    seed_products(client)

    p1_indexed, stock = fetch_product_with_stock(client, "sku-1")
    assert p1_indexed is True
    assert stock == 12
    print(f"Pattern 1 result: index-served={p1_indexed}, stock_level={stock}")

    update_stock(client, "sku-1", new_stock_level=11)  # => a real write, simulating one unit sold
    _p1_indexed_again, stock_after_sale = fetch_product_with_stock(client, "sku-1")
    assert stock_after_sale == 11  # => the write round-tripped correctly through the same index-served read
    print(f"After update_stock: stock_level={stock_after_sale}")

    p2_indexed, prices = fetch_category_cheapest_first(client, "electronics")
    assert p2_indexed is True
    assert prices == [9.99, 29.99]
    print(f"Pattern 2 result: index-served={p2_indexed}, prices={prices}")

    print("doc.py: both named access patterns are index-served and return the expected data -- PASSED")
    client.close()


if __name__ == "__main__":
    main()
