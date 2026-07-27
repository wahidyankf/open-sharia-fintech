"""Example 78: Capstone Preview - Document Access Pattern."""  # => co-08,co-17,co-19: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => enables the explicit MongoClient[dict[str, Any]] type parameter below (DD-39, pyright --strict)

from pymongo import MongoClient  # => co-18: pymongo, the official typed Python driver -- the capstone's own doc.py will build on exactly this

Document = dict[str, Any]  # => co-18: pymongo's own convention for "a MongoDB document" -- every field's own type varies per-document

# The capstone's own two named access patterns, previewed here (co-08):
ACCESS_PATTERN_1 = "fetch a product with its current stock level"  # => the capstone's dominant read #1
ACCESS_PATTERN_2 = "fetch every product in a given category, cheapest first"  # => the capstone's dominant read #2


def seed_products(client: MongoClient[Document]) -> None:  # => co-08: a shape derived FROM the two access patterns above
    """Seed products with fields chosen specifically to serve BOTH named access patterns."""  # => documents the contract
    collection = client["nosqldb"]["capstone_preview_products"]  # => co-08: a dedicated collection for this capstone preview
    collection.delete_many({})  # => resets state -- this example is fully self-contained
    collection.insert_many(
        [  # => co-08: stock_level and category+price are ON the document, ready for both patterns
            {"sku": "sku-1", "category": "electronics", "price": 29.99, "stock_level": 12},  # => in stock, serves pattern 1's stock-level check
            {"sku": "sku-2", "category": "electronics", "price": 9.99, "stock_level": 0},  # => OUT of stock, deliberately, and the CHEAPEST electronics item
            {"sku": "sku-3", "category": "books", "price": 14.50, "stock_level": 40},  # => a DIFFERENT category -- excluded from pattern 2's electronics query
        ]
    )  # => closes the insert_many() call -- 3 documents, spanning both patterns' own filter conditions
    collection.create_index("sku")  # => co-17: supports pattern 1 -- a single-document lookup by sku
    collection.create_index([("category", 1), ("price", 1)])  # => co-17: supports pattern 2 -- a compound index, category-then-price


def answer_pattern_1(client: MongoClient[Document], sku: str) -> tuple[bool, int]:  # => co-08: (index-served?, stock_level)
    """Answer pattern 1: fetch a product with its stock level, via an index-served single-document read."""  # => documents the contract
    collection = client["nosqldb"]["capstone_preview_products"]  # => selects the collection seed_products just populated
    explanation = collection.find({"sku": sku}).explain()  # => co-17: confirms the query is genuinely INDEX-served, not a collection scan
    index_served = explanation["queryPlanner"]["winningPlan"]["stage"] == "FETCH"  # => co-17: FETCH-from-IXSCAN means the sku index was used
    doc = collection.find_one({"sku": sku})  # => the actual single-document read
    assert doc is not None  # => confirms the product genuinely exists
    return index_served, doc["stock_level"]  # => hand back both the index-served flag and the stock level


def answer_pattern_2(client: MongoClient[Document], category: str) -> tuple[bool, list[float]]:  # => co-08: (index-served?, prices sorted ascending)
    """Answer pattern 2: fetch a category's products cheapest-first, via an index-served, pre-sorted read."""  # => documents contract
    collection = client["nosqldb"]["capstone_preview_products"]  # => selects the collection seed_products just populated
    cursor = collection.find({"category": category}).sort("price", 1)  # => co-08: the compound index ALREADY sorts by price ascending
    explanation = collection.find({"category": category}).sort("price", 1).explain()  # => confirms index usage for THIS shaped query too
    index_served = "IXSCAN" in str(explanation["queryPlanner"]["winningPlan"])  # => co-17: a simple, honest presence check across the plan's own stages
    prices = [doc["price"] for doc in cursor]  # => extracts prices in RETURN order -- already sorted by the index
    return index_served, prices  # => hand back both the index-served flag and the sorted price list


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client: MongoClient[Document] = MongoClient("mongodb://localhost:27017")  # => connects to a local MongoDB instance
    print(f"Pattern 1: {ACCESS_PATTERN_1}")  # => Output line
    print(f"Pattern 2: {ACCESS_PATTERN_2}")  # => Output line

    seed_products(client)  # => sets up the pattern-derived fixture, plus its supporting indexes
    p1_indexed, stock = answer_pattern_1(client, "sku-1")  # => co-08,co-17: runs and verifies pattern 1
    p2_indexed, prices = answer_pattern_2(client, "electronics")  # => co-08,co-17: runs and verifies pattern 2

    assert p1_indexed is True  # => co-17: pattern 1 was genuinely index-served
    assert stock == 12  # => confirms the correct stock level was returned
    assert p2_indexed is True  # => co-17: pattern 2 was genuinely index-served
    assert prices == [9.99, 29.99]  # => co-08: the electronics category, cheapest first, exactly as pattern 2 asks
    print(f"Pattern 1 result: index-served={p1_indexed}, stock_level={stock}")  # => Output: Pattern 1 result: index-served=True, stock_level=12
    print(f"Pattern 2 result: index-served={p2_indexed}, prices={prices}")  # => Output: Pattern 2 result: index-served=True, prices=[9.99, 29.99]
    print("Both named patterns index-served -- this is the shape the capstone's doc.py will build on")  # => Output line
    client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
