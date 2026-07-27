"""Example 60: Polyglot Persistence, Three Stores."""  # => co-26: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => enables the explicit MongoClient[dict[str, Any]] type parameter below (DD-39, pyright --strict)

import redis  # => co-26: Redis/Valkey for session state -- fast, TTL-native, disposable
from cassandra.cluster import Cluster, Session  # => co-26: Cassandra for event history -- append-heavy, partition-scoped
from pymongo import MongoClient  # => co-26: MongoDB for the catalog -- flexible document shape, secondary-indexable

Document = dict[str, Any]  # => co-26: pymongo's own convention for "a MongoDB document" -- every field's own type varies per-document


def use_redis_for_sessions(redis_client: redis.Redis) -> str:  # => co-26: session state -- exactly the access pattern Redis fits
    """Store and read a session token in Redis -- fast, TTL-native, exactly what Redis is FOR."""  # => documents the contract
    redis_client.set("session:user-1", "token-abc", ex=3600)  # => co-26: a disposable, TTL-bound value -- Redis's own core strength
    token = redis_client.get("session:user-1")  # => reads the SAME session back, as bytes | str | None
    if token is None:  # => co-26: no session found -- returns an empty string rather than raising
        return ""  # => the "no session" case, kept explicit rather than falling through
    return token.decode() if isinstance(token, bytes) else token  # => decodes only if the driver returned raw bytes


def use_mongo_for_catalog(mongo_client: MongoClient[Document]) -> dict[str, object]:  # => co-26: a product catalog -- MongoDB's flexible document shape fits
    """Store and read a product catalog entry in MongoDB -- flexible shape, secondary-indexable."""  # => documents contract
    catalog = mongo_client["nosqldb"]["catalog"]  # => co-26: no schema declared -- new product attributes can be added freely
    catalog.delete_many({"sku": "sku-42"})  # => resets state -- this example is fully self-contained
    catalog.insert_one({"sku": "sku-42", "name": "Wireless Mouse", "price": 25.99, "tags": ["electronics", "input-device"]})  # => co-26: a genuinely document-shaped record
    product = catalog.find_one({"sku": "sku-42"})  # => reads the SAME product back
    assert product is not None  # => confirms the catalog entry genuinely exists
    return {"name": product["name"], "price": product["price"]}  # => hand back the fields this function promises


def use_cassandra_for_event_history(session: Session) -> int:  # => co-26: append-heavy event history -- Cassandra's own wide-column strength
    """Insert and count events in Cassandra -- append-heavy, partition-scoped, exactly what Cassandra is FOR."""  # => documents contract
    session.execute(  # => a dedicated keyspace, replication_factor 1 on this single-node local cluster
        "CREATE KEYSPACE IF NOT EXISTS nosqldb WITH replication = "  # => the keyspace-level replication strategy clause
        "{'class': 'SimpleStrategy', 'replication_factor': 1}"  # => concatenated onto the line above -- ONE CQL statement string
    )  # => closes the execute() call -- the keyspace now exists, idempotently
    session.set_keyspace("nosqldb")  # => selects the keyspace for the statements below
    session.execute("DROP TABLE IF EXISTS user_events")  # => resets state -- this example is fully self-contained
    session.execute(  # => co-26: partitioned by user_id, clustered by event_id -- an append-heavy, time-ordered feed
        "CREATE TABLE user_events (user_id text, event_id int, event_type text, PRIMARY KEY ((user_id), event_id))"  # => partition key user_id, clustering key event_id
    )  # => closes the execute() call -- the table now exists with this exact partition + clustering layout
    for i, event_type in enumerate(["login", "view_product", "add_to_cart"]):  # => co-26: 3 events, appended in order
        session.execute(  # => co-26: each event is a cheap, sequential APPEND -- Cassandra's own write-path strength
            "INSERT INTO user_events (user_id, event_id, event_type) VALUES (%s, %s, %s)",  # => positional CQL placeholders
            ("user-1", i, event_type),  # => every event lands in user-1's own single partition, ordered by event_id
        )  # => closes this one execute() call -- runs 3 times, once per generated event
    rows = list(session.execute("SELECT event_type FROM user_events WHERE user_id = %s", ("user-1",)))  # => a single-partition read
    return len(rows)  # => hand back the count of events found for this user


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    redis_client = redis.Redis(host="localhost", port=6379, db=0)  # => co-26: connects to the SAME Valkey/Redis instance every prior Redis example used
    mongo_client = MongoClient("mongodb://localhost:27017")  # => co-26: connects to the SAME MongoDB instance every prior MongoDB example used
    cassandra_cluster = Cluster(["127.0.0.1"], port=9042)  # => co-26: connects to the SAME Cassandra cluster every prior Cassandra example used
    cassandra_session = cassandra_cluster.connect()  # => opens a session against that cluster

    session_token = use_redis_for_sessions(redis_client)  # => co-26: exercises Redis for exactly the access pattern it fits
    catalog_entry = use_mongo_for_catalog(mongo_client)  # => co-26: exercises MongoDB for exactly the access pattern it fits
    event_count = use_cassandra_for_event_history(cassandra_session)  # => co-26: exercises Cassandra for exactly the access pattern it fits

    assert session_token == "token-abc"  # => co-26: Redis served the session-state access pattern correctly
    assert catalog_entry == {"name": "Wireless Mouse", "price": 25.99}  # => co-26: MongoDB served the flexible-catalog access pattern correctly
    assert event_count == 3  # => co-26: Cassandra served the append-heavy event-history access pattern correctly
    print(f"Redis session:    {session_token}")  # => Output: Redis session:    token-abc
    print(f"MongoDB catalog:  {catalog_entry}")  # => Output: MongoDB catalog:  {'name': 'Wireless Mouse', 'price': 25.99}
    print(f"Cassandra events: {event_count} events recorded")  # => Output: Cassandra events: 3 events recorded
    print("One small app, THREE stores, each exercised for the access pattern it specifically fits -- deliberate, not accidental")  # => Output line

    redis_client.close()  # => always release what you open
    mongo_client.close()  # => always release what you open
    cassandra_cluster.shutdown()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
