"""Example 66: MongoDB Read Concern Tuning."""  # => co-07: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => enables the explicit MongoClient[dict[str, Any]] type parameter below (DD-39, pyright --strict)

from pymongo import MongoClient  # => co-07: pymongo, the official typed Python driver
from pymongo.read_concern import ReadConcern  # => co-07: ReadConcern is a typed, per-operation read-guarantee setting

Document = dict[str, Any]  # => co-07: pymongo's own convention for "a MongoDB document" -- every field's own type varies per-document


def read_with_concern(client: MongoClient[Document], level: str, probe_value: str) -> str | None:  # => co-07: reads at a GIVEN concern level
    """Read a document at the given read concern, returning the probe value found (or None)."""  # => documents the contract
    collection = client["nosqldb"]["read_concern_demo"].with_options(read_concern=ReadConcern(level=level))  # => co-07: PER-COLLECTION-HANDLE read concern
    doc = collection.find_one({"probe": probe_value})  # => co-07: the actual read, filtered at the configured concern
    return doc["probe"] if doc else None  # => hand back the matched probe value, or None if not visible at this level


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = MongoClient("mongodb://localhost:27017")  # => connects to a local MongoDB replica-set instance
    collection = client["nosqldb"]["read_concern_demo"]  # => selects the collection this example owns
    collection.delete_many({})  # => resets state -- this example is fully self-contained
    collection.insert_one({"probe": "committed-value"}, bypass_document_validation=False)  # => a normally-committed write

    local_result = read_with_concern(client, "local", "committed-value")  # => co-07: readConcern "local" -- the node's own current data, no cluster-wide check
    majority_result = read_with_concern(client, "majority", "committed-value")  # => co-07: readConcern "majority" -- only data acknowledged by a majority
    assert local_result == "committed-value"  # => co-07: on THIS single-node replica set, both levels see the same committed data
    assert majority_result == "committed-value"  # => co-07: both levels agree here -- no rollback scenario exists on a healthy single-node set
    print(f"readConcern 'local':    {local_result}")  # => Output: readConcern 'local':    committed-value
    print(f"readConcern 'majority': {majority_result}")  # => Output: readConcern 'majority': committed-value
    # => co-07: on THIS single-node local replica set, both levels agree because there is no genuine
    # => multi-node divergence to expose -- honestly, reproducing "local reads data a rollback could
    # => later discard" requires a real multi-node failover with a stale-primary rollback, which this
    # => local single-node setup cannot exercise; the DOCUMENTED distinction (verified against
    # => MongoDB's own manual) is that readConcern "local" returns the node's most recent data with NO
    # => guarantee it has been acknowledged by a majority -- if that node's data is later rolled back
    # => during a real failover (because it was never actually majority-committed), a "local" read could
    # => have observed data that effectively never durably existed; readConcern "majority" only ever
    # => returns data already acknowledged by a majority of the replica set, so it CANNOT observe
    # => anything a future rollback could discard
    print("Documented distinction (not reproducible on a single-node local set): 'local' may expose pre-rollback data; 'majority' never can")  # => Output line
    client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
