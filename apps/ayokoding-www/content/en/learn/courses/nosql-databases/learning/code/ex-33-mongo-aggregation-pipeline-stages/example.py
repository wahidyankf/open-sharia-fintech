"""Example 33: MongoDB Aggregation Pipeline Stages."""  # => co-19: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => enables the explicit MongoClient[dict[str, Any]] type parameter below (DD-39, pyright --strict)

from pymongo import MongoClient  # => co-19: pymongo, the official typed Python driver

Document = dict[str, Any]  # => co-19: pymongo's own convention for "a MongoDB document" -- every field's own type varies per-document


def seed_events(client: MongoClient[Document]) -> None:  # => a deterministic fixture across 3 event types
    """Reset and seed 6 events across 3 types, with varying severities."""  # => documents the contract
    collection = client["nosqldb"]["events"]  # => co-19: no schema declared for this collection
    collection.delete_many({})  # => resets state -- this example is fully self-contained
    collection.insert_many(
        [  # => co-19: 6 events, 3 distinct types, some low-severity to be filtered out
            {"type": "login", "severity": 3},  # => login event 1, severity >= 2 -- survives $match
            {"type": "login", "severity": 1},  # => login event 2, severity 1 -- excluded by $match below
            {"type": "error", "severity": 5},  # => error event 1, severity >= 2 -- survives $match
            {"type": "error", "severity": 4},  # => error event 2, severity >= 2 -- survives $match
            {"type": "error", "severity": 1},  # => severity 1 -- excluded by $match below
            {"type": "logout", "severity": 2},  # => logout's only event, severity >= 2 -- survives $match
        ]
    )  # => 6 events seeded, 2 with severity 1 -- exactly 2 must be dropped by stage 1's $match


def top_event_types_by_avg_severity(client: MongoClient[Document]) -> list[Document]:  # => co-19: 3-stage chained pipeline
    """Chain $match -> $group -> $sort, computing average severity per type, filtered and ranked."""  # => documents contract
    collection = client["nosqldb"]["events"]  # => selects the collection seed_events just populated
    pipeline = [  # => co-19: each stage's OUTPUT is the next stage's INPUT -- a data-flow pipeline, not nested SQL
        {"$match": {"severity": {"$gte": 2}}},  # => co-19: stage 1 -- drops the low-severity noise (severity 1)
        {"$group": {"_id": "$type", "avg_severity": {"$avg": "$severity"}}},  # => co-19: stage 2 -- averages PER remaining type
        {"$sort": {"avg_severity": -1}},  # => co-19: stage 3 -- highest average severity first
    ]  # => 3 chained stages, all server-side, in ONE round trip
    return list(collection.aggregate(pipeline))  # => co-19: ONE round trip runs all 3 stages server-side


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = MongoClient("mongodb://localhost:27017")  # => connects to a local MongoDB instance
    seed_events(client)  # => sets up the 6-event, 3-type fixture
    ranked = top_event_types_by_avg_severity(client)  # => runs the 3-stage chained pipeline
    for row in ranked:  # => prints the ranked, averaged, filtered result
        print(f"{row['_id']}: avg_severity={row['avg_severity']:.1f}")  # => Output line, one per event type
    assert ranked[0]["_id"] == "error"  # => co-19: error's average (4.5, only severity>=2 events counted) ranks highest
    assert ranked[-1]["_id"] == "logout"  # => co-19: logout's single event (severity 2) ranks lowest of the 3
    client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
