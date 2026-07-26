# Example 68: Preview: Friends-of-Friends from Python. (co-09)
from neo4j import GraphDatabase  # => driver package, `pip install neo4j`

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
# => a live connection -- swap the URI/credentials for your own setup


def seed(
    tx,
) -> None:  # => plants a small 2-hop chain this example bounds-checks against
    tx.run(  # => the write call itself
        "CREATE (:Person {name: 'Ada'})-[:KNOWS]->(:Person {name: 'Bob'})"  # => hop 1: Ada->Bob
        "-[:KNOWS]->(:Person {name: 'Cid'})"  # => hop 2: Bob->Cid, chained onto the same CREATE
    )  # => a 2-hop chain: Ada -> Bob -> Cid, matching Example 14's fixture shape


def friends_of_friends(
    tx, name: str
) -> list[str]:  # => the bounded traversal under test
    # co-09: *1..2 bounds the traversal to at most 2 hops -- friends AND friends-of-friends.
    result = tx.run(  # => the bounded-traversal query call itself
        "MATCH (a:Person {name: $name})-[:KNOWS*1..2]-(b:Person) RETURN DISTINCT b.name AS name",
        name=name,  # => binds $name -- the starting person's name
    )  # => end of the bounded-traversal query call
    return sorted(
        row["name"] for row in result
    )  # => sorted for a deterministic, checkable order


with (
    driver.session() as session
):  # => opens one session for both the seed write and the read
    session.execute_write(seed)  # => runs seed() as one write transaction
    result = session.execute_read(
        friends_of_friends, "Ada"
    )  # => runs the bounded query
    print(result)  # => hand-traced: Bob (1 hop) and Cid (2 hops) both fall within *1..2

driver.close()  # => releases the driver's connection pool cleanly
