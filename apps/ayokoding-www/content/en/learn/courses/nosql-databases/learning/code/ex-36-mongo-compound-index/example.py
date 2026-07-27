"""Example 36: MongoDB Compound Index."""  # => co-17: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => enables the explicit MongoClient[dict[str, Any]] type parameter below (DD-39, pyright --strict)

from pymongo import ASCENDING, MongoClient  # => co-17: ASCENDING names the sort direction explicitly, not a bare 1

Document = dict[str, Any]  # => co-17: pymongo's own convention for "a MongoDB document" -- every field's own type varies per-document


def seed_orders(client: MongoClient[Document]) -> None:  # => enough documents that the planner's index choice is measurable
    """Reset and seed 3000 orders across a small set of statuses and customers."""  # => documents the contract
    collection = client["nosqldb"]["orders_compound"]  # => co-17: a dedicated collection for this compound-index demonstration
    collection.delete_many({})  # => resets state -- this example is fully self-contained
    collection.insert_many(
        [  # => co-17: 3000 documents -- enough that an unindexed 2-field filter is genuinely more expensive
            {"customer_id": i % 50, "status": "paid" if i % 4 != 0 else "cancelled", "amount": i}  # => 50 distinct customers, 3/4 paid, spread across 3000 rows
            for i in range(3000)  # => generates all 3000 documents deterministically
        ]
    )  # => enough volume that COLLSCAN vs. IXSCAN genuinely differ in cost, not just in name


def explain_two_field_query(client: MongoClient[Document]) -> tuple[str, str]:  # => returns the winning index name, before/after
    """Run a 2-field equality query before and after a matching compound index."""  # => documents the contract
    collection = client["nosqldb"]["orders_compound"]  # => selects the collection seed_orders just populated
    query = {"customer_id": 7, "status": "paid"}  # => co-17: a 2-FIELD equality filter -- exactly what a compound index targets

    before = collection.find(query).explain()  # => co-17: explain() WITHOUT a matching compound index
    before_stage = before["queryPlanner"]["winningPlan"]["stage"]  # => co-17: no compound index exists -- expect COLLSCAN
    assert before_stage == "COLLSCAN"  # => co-17: confirms the baseline -- a full collection scan

    collection.create_index([("customer_id", ASCENDING), ("status", ASCENDING)])  # => co-17: ONE compound index covering BOTH fields
    after = collection.find(query).explain()  # => the SAME query, re-explained now that the compound index exists
    after_index_name = after["queryPlanner"]["winningPlan"]["inputStage"]["indexName"]  # => co-17: the specific index the planner chose
    assert after_index_name == "customer_id_1_status_1"  # => co-17: MongoDB's default name -- field_direction pairs joined by underscores

    return before_stage, after_index_name  # => hand both results back for the caller to print


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = MongoClient("mongodb://localhost:27017")  # => connects to a local MongoDB instance
    seed_orders(client)  # => sets up the 3000-document fixture
    before_stage, after_index_name = explain_two_field_query(client)  # => runs the before/after compound-index comparison
    print(f"Before compound index: {before_stage} | After: index '{after_index_name}' selected")  # => Output: Before compound index: COLLSCAN | After: index 'customer_id_1_status_1' selected
    client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
