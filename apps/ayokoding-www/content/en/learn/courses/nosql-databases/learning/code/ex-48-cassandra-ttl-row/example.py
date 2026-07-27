"""Example 48: Cassandra TTL Row."""  # => co-24: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import time  # => co-24: a real sleep past the TTL window -- the expiry must genuinely elapse, not be simulated

from cassandra.cluster import Cluster, Session  # => co-24: cassandra-driver, the Apache Software Foundation-maintained Python driver


def setup_sessions_table(session: Session) -> None:  # => co-24: a table this example owns exclusively
    """Create a dedicated table for this TTL demonstration."""  # => documents the contract, no runtime output
    session.execute(  # => a dedicated keyspace, replication_factor 1 on this single-node local cluster
        "CREATE KEYSPACE IF NOT EXISTS nosqldb WITH replication = "  # => the keyspace-level replication strategy clause
        "{'class': 'SimpleStrategy', 'replication_factor': 1}"  # => concatenated onto the line above -- ONE CQL statement string
    )  # => closes the execute() call -- the keyspace now exists, idempotently
    session.set_keyspace("nosqldb")  # => selects the keyspace for the statements below
    session.execute("DROP TABLE IF EXISTS ttl_sessions")  # => resets state -- this example is fully self-contained
    session.execute("CREATE TABLE ttl_sessions (session_id text PRIMARY KEY, auth_token text)")  # => a minimal table for this demonstration


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    cluster = Cluster(["127.0.0.1"], port=9042)  # => connects to the local single-node Cassandra 5.0 cluster
    session = cluster.connect()  # => opens a session against that cluster
    setup_sessions_table(session)  # => sets up the dedicated table fixture

    session.execute(  # => co-24: USING TTL <seconds> -- Cassandra auto-expires this ROW after the window elapses
        "INSERT INTO ttl_sessions (session_id, auth_token) VALUES (%s, %s) USING TTL 5",  # => note: "token" alone is a RESERVED CQL word -- "auth_token" sidesteps it
        ("sess-99", "tok-abc"),  # => bound values -- the row this TTL applies to
    )  # => closes the execute() call -- this ONE row now carries its own 5-second TTL, other rows are unaffected
    row_before = session.execute("SELECT auth_token FROM ttl_sessions WHERE session_id = %s", ("sess-99",)).one()  # => reads immediately after insert
    assert row_before is not None and row_before.auth_token == "tok-abc"  # => co-24: the row is present right after the TTL insert, well before expiry
    print(f"Immediately after insert (TTL=5s): token={row_before.auth_token}")  # => Output: Immediately after insert (TTL=5s): token=tok-abc

    time.sleep(6)  # => co-24: waits PAST the 5-second TTL window -- a genuine elapsed expiry, not a simulated one
    row_after = session.execute("SELECT auth_token FROM ttl_sessions WHERE session_id = %s", ("sess-99",)).one()  # => reads again, after the TTL elapsed
    assert row_after is None  # => co-24: the row is GONE -- Cassandra auto-purged it once the TTL window passed
    print(f"After the 5-second TTL elapses: row present = {row_after is not None}")  # => Output: After the 5-second TTL elapses: row present = False
    cluster.shutdown()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
