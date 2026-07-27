"""Example 58: Cassandra Lightweight Transaction."""  # => co-27: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from cassandra.cluster import Cluster, Session  # => co-27: cassandra-driver, the Apache Software Foundation-maintained Python driver


def setup_reservations_table(session: Session) -> None:  # => co-27: a table this example owns exclusively
    """Create a dedicated table for this lightweight-transaction demonstration."""  # => documents the contract, no runtime output
    session.execute(  # => a dedicated keyspace, replication_factor 1 on this single-node local cluster
        "CREATE KEYSPACE IF NOT EXISTS nosqldb WITH replication = "  # => the keyspace-level replication strategy clause
        "{'class': 'SimpleStrategy', 'replication_factor': 1}"  # => concatenated onto the line above -- ONE CQL statement string
    )  # => closes the execute() call -- the keyspace now exists, idempotently
    session.set_keyspace("nosqldb")  # => selects the keyspace for the statements below
    session.execute("DROP TABLE IF EXISTS seat_reservations")  # => resets state -- this example is fully self-contained
    session.execute("CREATE TABLE seat_reservations (seat_id text PRIMARY KEY, reserved_by text)")  # => a minimal table for this demonstration


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    cluster = Cluster(["127.0.0.1"], port=9042)  # => connects to the local single-node Cassandra 5.0 cluster
    session = cluster.connect()  # => opens a session against that cluster
    setup_reservations_table(session)  # => sets up the dedicated table fixture

    first_insert = session.execute(  # => co-27: IF NOT EXISTS -- a Paxos-backed compare-and-set, NOT a plain INSERT
        "INSERT INTO seat_reservations (seat_id, reserved_by) VALUES (%s, %s) IF NOT EXISTS",  # => the conditional CQL statement text
        ("seat-12A", "alice"),  # => alice claims seat-12A first
    ).one()  # => co-27: LWTs return a row describing whether the condition held
    assert first_insert.applied is True  # => co-27: [applied] = true -- seat-12A did not exist yet, so alice's reservation succeeded
    print(f"First reservation for seat-12A by alice: applied = {first_insert.applied}")  # => Output: First reservation for seat-12A by alice: applied = True

    second_insert = session.execute(  # => co-27: the SAME conditional insert, attempted by a SECOND, conflicting reservation
        "INSERT INTO seat_reservations (seat_id, reserved_by) VALUES (%s, %s) IF NOT EXISTS",  # => the identical conditional CQL statement text
        ("seat-12A", "bob"),  # => bob tries to claim the SAME seat second
    ).one()  # => co-27: bob's attempt on the SAME key, now that alice already holds it
    assert second_insert.applied is False  # => co-27: [applied] = false -- seat-12A ALREADY exists, bob's conditional insert is REJECTED
    print(f"Second reservation for seat-12A by bob:   applied = {second_insert.applied}")  # => Output: Second reservation for seat-12A by bob:   applied = False
    print(
        f"Row Cassandra returned instead: seat_id={second_insert.seat_id}, reserved_by={second_insert.reserved_by} (the EXISTING owner, not bob)"
    )  # => Output: Row Cassandra returned instead: seat_id=seat-12A, reserved_by=alice (the EXISTING owner, not bob)
    # => co-27: on a REJECTED LWT, Cassandra returns the row that CAUSED the rejection -- this is how a
    # => client learns WHO already holds the seat without a separate follow-up read; note (per this
    # => topic's own accuracy discipline) only the QUALITATIVE cost matters here -- "LWTs are expensive,
    # => reserve them for genuinely contested writes" -- not a specific latency number, since Paxos-backed
    # => coordination cost varies heavily by cluster topology and contention
    cluster.shutdown()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
