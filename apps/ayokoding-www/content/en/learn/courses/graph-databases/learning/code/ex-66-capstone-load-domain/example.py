# Example 66: Preview: Load the Capstone Domain. (co-06, co-20)
# A SMALL preview of the capstone's own load.py -- same MERGE-based loading idea, a tiny
# fixed dataset here, standing in for the capstone's larger one.
from neo4j import GraphDatabase  # => driver package, `pip install neo4j`

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
# => a live connection -- swap the URI/credentials for your own setup

PEOPLE = ["Ada", "Bob"]  # => 2 people to load
ITEMS = ["Keyboard"]  # => 1 item to load
BOUGHT = [("Ada", "Keyboard")]  # => 1 BOUGHT edge to load


def load(
    tx,
) -> None:  # => builds all three MERGE-based writes below, in one write transaction
    # co-06/co-20: every write below is MERGE, not CREATE -- reruns never duplicate anything.
    for name in PEOPLE:  # => one MERGE per person in the source list
        tx.run(
            "MERGE (:User {name: $name})", name=name
        )  # => idempotent per-person write (co-06)
    for item in ITEMS:  # => one MERGE per item in the source list
        tx.run("MERGE (:Item {name: $item})", item=item)  # => idempotent per-item write
    for (
        buyer,
        item,
    ) in BOUGHT:  # => one MATCH+MERGE per (buyer, item) pair in the source list
        # a single MATCH + MERGE statement -- MATCH finds both endpoints, MERGE connects them
        tx.run(
            "MATCH (u:User {name: $buyer}), (i:Item {name: $item}) MERGE (u)-[:BOUGHT]->(i)",
            buyer=buyer,  # => binds $buyer in the query string above
            item=item,  # => binds $item in the query string above
        )  # => idempotent per-edge write -- reruns of this whole script never duplicate anything


with (
    driver.session() as session
):  # => opens one session for both the write and the verify read
    session.execute_write(
        load
    )  # => runs the whole load() function as one write transaction
    counts = session.execute_read(  # => a second, read-only transaction verifying the load
        lambda tx: tx.run(  # => the verification query itself, run inline as a lambda
            "MATCH (u:User) WITH count(u) AS users "  # => counts every User node just loaded
            "MATCH (i:Item) WITH users, count(i) AS items "  # => counts every Item node loaded
            "MATCH ()-[r:BOUGHT]->() RETURN users, items, count(r) AS bought"
            # => counts every BOUGHT relationship, carrying the two prior counts along via WITH
        ).single()  # => exactly one summary row expected back
    )  # => end of the verification read transaction
    print(
        dict(counts)
    )  # => {'users': 2, 'items': 1, 'bought': 1} -- matches PEOPLE/ITEMS/BOUGHT

driver.close()  # => releases the driver's connection pool cleanly
