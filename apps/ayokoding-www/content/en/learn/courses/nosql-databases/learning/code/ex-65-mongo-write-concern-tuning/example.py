"""Example 65: MongoDB Write Concern Tuning."""  # => co-07: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import time  # => co-07: measures wall-clock latency at each write concern, honestly, on this replica-set instance

from typing import Any  # => enables the explicit MongoClient[dict[str, Any]] type parameter below (DD-39, pyright --strict)

from pymongo import MongoClient, WriteConcern  # => co-07: WriteConcern is a typed, per-operation acknowledgment setting

Document = dict[str, Any]  # => co-07: pymongo's own convention for "a MongoDB document" -- every field's own type varies per-document


def write_with_concern(client: MongoClient[Document], w: int | str) -> float:  # => co-07: writes at a GIVEN concern level, returns elapsed seconds
    """Insert one document with the given write concern, returning wall-clock latency."""  # => documents the contract
    collection = client["nosqldb"]["write_concern_demo"].with_options(write_concern=WriteConcern(w=w))  # => co-07: PER-COLLECTION-HANDLE write concern
    start = time.perf_counter()  # => marks the start of the timed write
    collection.insert_one({"probe": w})  # => co-07: the actual timed write, acknowledged per the configured concern
    return time.perf_counter() - start  # => elapsed wall-clock seconds for this one write


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = MongoClient("mongodb://localhost:27017")  # => connects to a local MongoDB replica-set instance
    client["nosqldb"]["write_concern_demo"].delete_many({})  # => resets state -- this example is fully self-contained

    latency_w1 = write_with_concern(client, 1)  # => co-07: w=1 -- acknowledged as soon as the PRIMARY alone applies it
    latency_majority = write_with_concern(client, "majority")  # => co-07: w="majority" -- acknowledged only once a MAJORITY of replica-set members apply it

    print(f"w=1:         {latency_w1 * 1000:.2f}ms")  # => Output line -- exact ms machine-dependent
    print(f"w='majority':{latency_majority * 1000:.2f}ms")  # => Output line -- exact ms machine-dependent
    # => co-07: on a SINGLE-NODE replica set (this local instance), "majority" reduces to that one
    # => node's own ack, so the two levels are not meaningfully different HERE in latency -- on a real
    # => multi-node replica set, w="majority" waits for additional replicas to apply the write before
    # => acknowledging, which is strictly slower but survives a primary failure without losing the write

    count = client["nosqldb"]["write_concern_demo"].count_documents({})  # => confirms BOTH writes landed, regardless of concern level
    assert count == 2  # => co-07: both the w=1 write and the w="majority" write succeeded and are visible
    print(f"Both writes visible: {count} documents in write_concern_demo")  # => Output: Both writes visible: 2 documents in write_concern_demo
    print("w=1 acknowledges as soon as the primary applies the write; w='majority' waits for a majority of the replica set to apply it too")  # => Output line
    client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
