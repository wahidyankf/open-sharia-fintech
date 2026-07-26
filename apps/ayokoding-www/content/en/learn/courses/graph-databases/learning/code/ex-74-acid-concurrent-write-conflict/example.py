# Example 74: Concurrent Write Conflict. (co-19)
import threading  # => stdlib, used to run two overlapping transactions concurrently
from neo4j import GraphDatabase  # => driver package, `pip install neo4j`
from neo4j.exceptions import (
    TransientError,
)  # => the exception Neo4j raises on a lock conflict

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
# => a live connection -- swap the URI/credentials for your own setup


def seed(
    tx,
) -> None:  # => plants the single shared counter both threads race to increment
    tx.run(
        "CREATE (:Counter {name: 'shared', value: 0})"
    )  # => one node, both threads target it


def slow_increment(
    tx, sleep_seconds: float
) -> None:  # => the write both threads run concurrently
    tx.run("MATCH (c:Counter {name: 'shared'}) SET c.value = c.value + 1")
    # => a real driver would hold the write lock on 'shared' for the WHOLE transaction's duration;
    # sleep_seconds here stands in for that duration to make the overlap deliberate and visible
    import time  # => stdlib, imported here only for the sleep() call immediately below

    time.sleep(
        sleep_seconds
    )  # => holds this transaction open, forcing the second thread to wait


results: dict[str, str] = {}  # => shared dict both threads write their own outcome into


def run_thread(
    name: str, sleep_seconds: float
) -> None:  # => one thread's whole run, start to finish
    with (
        driver.session() as session
    ):  # => each thread gets its OWN session, deliberately
        try:
            session.execute_write(
                slow_increment, sleep_seconds
            )  # => the racing write itself
            results[name] = (
                "committed"  # => this thread's transaction won the lock and committed
            )
        except TransientError as err:
            # => Neo4j's own locking surfaces a concurrent-modification conflict as this exact
            # exception type -- the SECOND transaction to reach the lock is the one that sees it
            results[name] = (
                f"failed: {err.code}"  # => records the conflict, does not crash the script
            )


with (
    driver.session() as session
):  # => a separate, single session for the one-time seed write
    session.execute_write(
        seed
    )  # => plants the shared counter before either thread starts racing

t1 = threading.Thread(
    target=run_thread, args=("t1", 0.5)
)  # => thread 1, half-second hold
t2 = threading.Thread(
    target=run_thread, args=("t2", 0.5)
)  # => thread 2, half-second hold, overlapping
t1.start()  # => starts thread 1's transaction
t2.start()  # => starts thread 2's transaction -- overlaps with thread 1's still-open write
t1.join()  # => blocks until thread 1 finishes
t2.join()  # => blocks until thread 2 finishes
print(
    results
)  # => ONE thread commits; the other either fails with TransientError or retries

driver.close()  # => releases the driver's connection pool cleanly
