"""Example 71: Wide-Column vs. Document Tradeoff."""  # => co-22,co-18: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => enables the explicit MongoClient[dict[str, Any]] type parameter below (DD-39, pyright --strict)

from cassandra.cluster import Cluster, Session  # => co-22: cassandra-driver, the Apache Software Foundation-maintained Python driver
from pymongo import MongoClient  # => co-18: pymongo, the official typed Python driver

Document = dict[str, Any]  # => co-18: pymongo's own convention for "a MongoDB document" -- every field's own type varies per-document

MONGO_ARRAY_SIZE_LIMIT_BYTES = 16 * 1024 * 1024  # => co-18: MongoDB's HARD 16MB document size ceiling -- an embedded array shares this budget


def setup_cassandra_feed(session: Session) -> None:  # => co-22: an UNBOUNDED wide-column partition -- new rows just append, no document-size ceiling
    """Create a Cassandra table modeling an unbounded activity feed as a partition + clustering key."""  # => documents the contract
    session.execute(  # => a dedicated keyspace, replication_factor 1 on this single-node local cluster
        "CREATE KEYSPACE IF NOT EXISTS nosqldb WITH replication = "  # => the keyspace-level replication strategy clause
        "{'class': 'SimpleStrategy', 'replication_factor': 1}"  # => concatenated onto the line above -- ONE CQL statement string
    )  # => closes the execute() call -- the keyspace now exists, idempotently
    session.set_keyspace("nosqldb")  # => selects the keyspace for the statements below
    session.execute("DROP TABLE IF EXISTS activity_feed_wide")  # => resets state -- this example is fully self-contained
    session.execute(  # => co-22: user_id partitions, event_id clusters -- appending a new event is a CHEAP, bounded-cost write
        "CREATE TABLE activity_feed_wide (user_id text, event_id int, event_text text, PRIMARY KEY ((user_id), event_id))"  # => partition key user_id, clustering key event_id
    )  # => closes the execute() call -- the table now exists with this exact partition + clustering layout


def append_to_cassandra_feed(session: Session, event_count: int) -> None:  # => co-22: each event is an INDEPENDENT row -- no read-modify-write of a growing blob
    """Append event_count events to the Cassandra feed, one INSERT each."""  # => documents the contract, no runtime output
    for i in range(event_count):  # => co-22: each append is its OWN small, independent write
        session.execute(  # => co-22: an INSERT of a NEW row -- the cost of appending event #10,000 is IDENTICAL to appending event #1
            "INSERT INTO activity_feed_wide (user_id, event_id, event_text) VALUES (%s, %s, %s)",  # => positional CQL placeholders
            ("user-1", i, f"event-{i}"),  # => every event lands in user-1's own single partition, ordered by event_id
        )  # => closes this one execute() call -- runs once per appended event


def setup_and_append_mongo_feed(client: MongoClient[Document], event_count: int) -> None:  # => co-18: an EMBEDDED array -- grows the WHOLE document each append
    """Reset and append event_count events into a single MongoDB document's embedded array."""  # => documents the contract
    collection = client["nosqldb"]["activity_feed_embedded"]  # => co-18: a dedicated collection for the embedded-array shape
    collection.delete_many({})  # => resets state -- this example is fully self-contained
    collection.insert_one({"user_id": "user-1", "events": []})  # => co-18: starts with an EMPTY embedded array
    for i in range(event_count):  # => co-18: each append re-writes (grows) the SAME document's array field
        collection.update_one(  # => co-18: $push re-reads and re-writes the WHOLE document's array field under the hood
            {"user_id": "user-1"},
            {"$push": {"events": f"event-{i}"}},  # => co-18: the growing array lives INSIDE the single parent document
        )  # => closes this one update_one() call -- runs once per appended event, growing the array further each time


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    cluster = Cluster(["127.0.0.1"], port=9042)  # => connects to the local single-node Cassandra 5.0 cluster
    cassandra_session = cluster.connect()  # => opens a session against that cluster
    mongo_client = MongoClient("mongodb://localhost:27017")  # => connects to a local MongoDB instance

    event_count = 50  # => a small but sufficient sample -- this example is about the SHAPE of the cost, not raw scale
    setup_cassandra_feed(cassandra_session)  # => sets up the wide-column feed table
    append_to_cassandra_feed(cassandra_session, event_count)  # => co-22: 50 independent row appends
    setup_and_append_mongo_feed(mongo_client, event_count)  # => co-18: 50 array-growing document updates

    cassandra_rows = list(cassandra_session.execute("SELECT event_id FROM activity_feed_wide WHERE user_id = %s", ("user-1",)))  # => a single-partition read
    mongo_doc = mongo_client["nosqldb"]["activity_feed_embedded"].find_one({"user_id": "user-1"})  # => a single-document read
    assert len(cassandra_rows) == event_count  # => co-22: all 50 events served by ONE partition-scoped query
    assert mongo_doc is not None and len(mongo_doc["events"]) == event_count  # => co-18: all 50 events served by ONE document read
    print(f"Cassandra wide-column feed: {len(cassandra_rows)} events, served by one partition-scoped query")  # => Output: Cassandra wide-column feed: 50 events, served by one partition-scoped query
    print(f"MongoDB embedded-array feed: {len(mongo_doc['events'])} events, served by one document read")  # => Output: MongoDB embedded-array feed: 50 events, served by one document read

    # As the feed grows WITHOUT BOUND, the two shapes' update cost diverges sharply:
    print(f"Cassandra: appending event #{event_count + 1} costs the SAME as appending event #1 -- an independent row, no shared blob to re-write")  # => Output line
    print(
        f"MongoDB:   appending event #{event_count + 1} re-writes the WHOLE growing array field, and the document has a hard {MONGO_ARRAY_SIZE_LIMIT_BYTES // (1024 * 1024)}MB ceiling"
    )  # => Output: MongoDB:   appending event #51 re-writes the WHOLE growing array field, and the document has a hard 16MB ceiling
    # => co-22,co-18: Cassandra's wide-column partition has NO document-size ceiling analogous to
    # => MongoDB's 16MB limit -- a feed that grows genuinely without bound (years of activity history)
    # => is the textbook case FOR a wide-column shape over an embedded-array shape, even though BOTH
    # => shapes serve the current read equally well at this example's small scale

    cluster.shutdown()  # => always release what you open
    mongo_client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
