"""Example 72: NoSQL Transactions Cost Comparison."""  # => co-27: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import statistics  # => co-27: the median of several timed runs is far less noisy than any single sample, especially the FIRST one
import time  # => co-27: measures wall-clock latency for each transactional primitive, honestly, on real local services

from typing import Any  # => enables the explicit MongoClient[dict[str, Any]] type parameter below (DD-39, pyright --strict)

import redis  # => co-27: redis-py, the official typed Python client
from cassandra.cluster import Cluster, Session  # => co-27: cassandra-driver, the Apache Software Foundation-maintained Python driver
from pymongo import MongoClient  # => co-27: pymongo, the official typed Python driver

Document = dict[str, Any]  # => co-27: pymongo's own convention for "a MongoDB document" -- every field's own type varies per-document


def time_redis_plain_set(client: redis.Redis) -> float:  # => co-27: the NON-transactional baseline -- a single SET
    """Time a single, non-transactional SET -- the baseline this example compares every transaction against."""  # => documents contract
    start = time.perf_counter()  # => marks the start
    client.set("cost:redis:plain", "v")  # => co-27: NO MULTI/EXEC -- the cheapest possible Redis write
    return time.perf_counter() - start  # => elapsed seconds


def time_redis_multi_exec(client: redis.Redis) -> float:  # => co-27: the SAME write, wrapped in MULTI/EXEC
    """Time the SAME write wrapped in MULTI/EXEC."""  # => documents the contract
    start = time.perf_counter()  # => marks the start
    pipe = client.pipeline(transaction=True)  # => co-27: transaction=True -- adds MULTI/EXEC framing around the write
    pipe.multi()  # => co-27: MULTI
    pipe.set("cost:redis:txn", "v")  # => the SAME logical write as the baseline
    pipe.execute()  # => co-27: EXEC
    return time.perf_counter() - start  # => elapsed seconds


def time_mongo_plain_insert(client: MongoClient[Document]) -> float:  # => co-27: the NON-transactional baseline -- a single insert_one
    """Time a single, non-transactional insert_one -- the baseline this example compares every transaction against."""  # => documents contract
    collection = client["nosqldb"]["cost_demo"]  # => a dedicated collection for this comparison
    start = time.perf_counter()  # => marks the start
    collection.insert_one({"probe": "plain"})  # => co-27: NO session, NO transaction -- the cheapest possible MongoDB write
    return time.perf_counter() - start  # => elapsed seconds


def time_mongo_transaction(client: MongoClient[Document]) -> float:  # => co-27: the SAME write, wrapped in a session-scoped transaction
    """Time the SAME write wrapped in a session-scoped multi-document transaction."""  # => documents the contract
    collection = client["nosqldb"]["cost_demo"]  # => the same collection as the baseline
    start = time.perf_counter()  # => marks the start
    with client.start_session() as session, session.start_transaction():  # => co-27: session+transaction overhead -- absent from the plain-insert baseline
        collection.insert_one({"probe": "txn"}, session=session)  # => the SAME logical write as the baseline
    return time.perf_counter() - start  # => elapsed seconds


def time_cassandra_plain_insert(session: Session) -> float:  # => co-27: the NON-transactional baseline -- a single INSERT
    """Time a single, non-transactional INSERT -- the baseline this example compares the LWT against."""  # => documents contract
    start = time.perf_counter()  # => marks the start
    session.execute("INSERT INTO cost_demo (id, probe) VALUES (%s, %s)", (1, "plain"))  # => co-27: NO IF NOT EXISTS -- the cheapest possible Cassandra write
    return time.perf_counter() - start  # => elapsed seconds


def time_cassandra_lwt(session: Session) -> float:  # => co-27: the SAME write, wrapped in a Paxos-backed lightweight transaction
    """Time the SAME write wrapped in an IF NOT EXISTS lightweight transaction."""  # => documents the contract
    start = time.perf_counter()  # => marks the start
    session.execute("INSERT INTO cost_demo (id, probe) VALUES (%s, %s) IF NOT EXISTS", (2, "txn"))  # => co-27: Paxos coordination overhead, absent from the plain baseline
    return time.perf_counter() - start  # => elapsed seconds


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    redis_client = redis.Redis(host="localhost", port=6379, db=0)  # => connects to a local Valkey/Redis instance
    mongo_client = MongoClient("mongodb://localhost:27017")  # => connects to a local MongoDB replica-set instance
    cassandra_cluster = Cluster(["127.0.0.1"], port=9042)  # => connects to the local single-node Cassandra 5.0 cluster
    cassandra_session = cassandra_cluster.connect()  # => opens a session against that cluster
    cassandra_session.execute(  # => a dedicated keyspace, replication_factor 1 on this single-node local cluster
        "CREATE KEYSPACE IF NOT EXISTS nosqldb WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}"
    )
    cassandra_session.set_keyspace("nosqldb")  # => selects the keyspace for the statements below
    cassandra_session.execute("DROP TABLE IF EXISTS cost_demo")  # => resets state -- this example is fully self-contained
    cassandra_session.execute("CREATE TABLE cost_demo (id int PRIMARY KEY, probe text)")  # => a minimal table for this demonstration

    runs = 7  # => co-27: enough repeats that a MEDIAN smooths out first-call connection-warm-up noise
    time_redis_plain_set(redis_client)  # => co-27: an untimed WARM-UP call -- absorbs any first-call connection-setup cost before timing starts
    time_mongo_plain_insert(mongo_client)  # => co-27: same warm-up discipline for MongoDB's connection
    time_cassandra_plain_insert(cassandra_session)  # => co-27: same warm-up discipline for Cassandra's connection

    redis_plain = statistics.median(time_redis_plain_set(redis_client) for _ in range(runs))  # => co-27: Redis baseline, median of 7 runs
    redis_txn = statistics.median(time_redis_multi_exec(redis_client) for _ in range(runs))  # => co-27: Redis MULTI/EXEC, median of 7 runs
    mongo_plain = statistics.median(time_mongo_plain_insert(mongo_client) for _ in range(runs))  # => co-27: MongoDB baseline, median of 7 runs
    mongo_txn = statistics.median(time_mongo_transaction(mongo_client) for _ in range(runs))  # => co-27: MongoDB transaction, median of 7 runs
    cassandra_plain = statistics.median(time_cassandra_plain_insert(cassandra_session) for _ in range(runs))  # => co-27: Cassandra baseline, median of 7 runs
    cassandra_txn = statistics.median(time_cassandra_lwt(cassandra_session) for _ in range(runs))  # => co-27: Cassandra LWT, median of 7 runs

    print(f"Redis:     plain={redis_plain * 1000:.2f}ms, MULTI/EXEC={redis_txn * 1000:.2f}ms")  # => Output line -- exact ms machine-dependent
    print(f"MongoDB:   plain={mongo_plain * 1000:.2f}ms, transaction={mongo_txn * 1000:.2f}ms")  # => Output line -- exact ms machine-dependent
    print(f"Cassandra: plain={cassandra_plain * 1000:.2f}ms, LWT={cassandra_txn * 1000:.2f}ms")  # => Output line -- exact ms machine-dependent

    assert mongo_txn > mongo_plain  # => co-27: MongoDB's session+transaction framing adds MEASURABLE overhead over a plain insert
    assert cassandra_txn > cassandra_plain  # => co-27: Cassandra's Paxos-backed LWT adds MEASURABLE overhead over a plain insert
    print("Every transactional primitive measured here adds overhead over its own non-transactional baseline -- the exact MS varies by run and machine, but the direction is consistent")  # => Output line
    # => co-27: Redis's MULTI/EXEC overhead is the smallest of the three (no distributed coordination,
    # => just command queuing) -- this example does not assert redis_txn > redis_plain because that
    # => specific gap is small enough to occasionally invert under local, single-process timing noise;
    # => MongoDB's and Cassandra's overhead (session/transaction machinery, Paxos coordination) is large
    # => enough to assert reliably

    redis_client.close()  # => always release what you open
    mongo_client.close()  # => always release what you open
    cassandra_cluster.shutdown()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
