# Example 22: ACID Transaction Rollback from Python. (co-19)
from neo4j import GraphDatabase  # => driver package, `pip install neo4j`
from neo4j.exceptions import (
    ClientError,
)  # => the exception type a constraint violation raises

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
# => a live connection -- swap the URI/credentials for your own setup


def two_writes_second_fails(tx) -> None:
    # BOTH writes below run inside the SAME transaction -- that is what execute_write does.
    tx.run("CREATE (:Person {name: 'Ada'})")  # => write #1: would succeed alone
    # write #2 deliberately violates the person_name constraint from Example 20,
    # forcing an error INSIDE the same transaction as write #1 above.
    tx.run(
        "CREATE (:Person {name: 'Ada'})"
    )  # => write #2: duplicate -> raises ClientError


with driver.session() as session:
    # => opens a driver session -- NOT yet a transaction on its own
    try:
        session.execute_write(two_writes_second_fails)
        # => execute_write wraps the whole function in ONE transaction -- any raised
        # exception inside it triggers an automatic rollback of EVERYTHING in that transaction
    except ClientError as err:
        print(
            "caught:", err.code
        )  # => confirms the failure was detected, not swallowed

    count = session.execute_read(
        # => a fresh READ transaction, separate from the failed write transaction above
        lambda tx: tx.run(
            "MATCH (p:Person {name: 'Ada'}) RETURN count(p) AS c"
        ).single()["c"]
    )
    print(
        "Ada node count after rollback:", count
    )  # => proves write #1 did NOT survive either

driver.close()
# => releases the driver's connection pool cleanly
