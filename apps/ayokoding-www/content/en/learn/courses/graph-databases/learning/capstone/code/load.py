# Capstone Step 1: Load the Domain via Cypher MERGE. (co-01, co-06, co-11)
# Loads a small social + commerce graph: 5 people, 3 items, 5 KNOWS edges, 4 BOUGHT edges --
# every write below is MERGE, not CREATE, so rerunning this script never duplicates anything.
from neo4j import GraphDatabase  # => driver package, `pip install neo4j`

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
# => a live connection -- swap the URI/credentials for your own setup

PEOPLE = ["Ada", "Bob", "Cid", "Dee", "Zoe"]  # => 5 people to load
ITEMS = ["Keyboard", "Monitor", "Mousepad"]  # => 3 items to load
KNOWS_EDGES = [
    ("Ada", "Bob"),  # => the base chain, hop 1
    ("Bob", "Cid"),  # => the base chain, hop 2
    ("Cid", "Dee"),  # => the base chain, hop 3
    ("Ada", "Zoe"),  # => a separate 1-hop branch off Ada
    (
        "Ada",
        "Cid",
    ),  # => a SHORTCUT -- this is what makes the shortest path to Dee 2 hops, not 3
]  # => 5 KNOWS edges total
BOUGHT_EDGES = [
    (
        "Ada",
        "Keyboard",
    ),  # => Ada's only purchase -- the recommendation's starting point
    (
        "Bob",
        "Keyboard",
    ),  # => Bob shares Ada's Keyboard purchase -- the co-occurrence signal
    (
        "Bob",
        "Mousepad",
    ),  # => Bob's EXTRA purchase -- the eventual recommendation candidate
    (
        "Cid",
        "Monitor",
    ),  # => an UNRELATED purchase -- Cid never bought Keyboard, so is not a co-buyer
]  # => 4 BOUGHT edges total


def load(tx) -> None:  # => the whole load, run as one write transaction
    for name in PEOPLE:  # => one MERGE per person
        tx.run(
            "MERGE (:Person {name: $name})", name=name
        )  # => idempotent per-person write (co-06)
    for item in ITEMS:  # => one MERGE per item
        tx.run("MERGE (:Item {name: $item})", item=item)  # => idempotent per-item write
    for a, b in KNOWS_EDGES:  # => one MATCH+MERGE per KNOWS edge
        tx.run(  # => the KNOWS edge write call itself
            "MATCH (a:Person {name: $a}), (b:Person {name: $b}) MERGE (a)-[:KNOWS]->(b)",
            a=a,  # => binds $a -- the edge's source person
            b=b,  # => binds $b -- the edge's target person
        )  # => idempotent per-edge write -- co-01/co-11: a typed, directed relationship
    for person, item in BOUGHT_EDGES:  # => one MATCH+MERGE per BOUGHT edge
        tx.run(  # => the BOUGHT edge write call itself
            "MATCH (p:Person {name: $person}), (i:Item {name: $item}) MERGE (p)-[:BOUGHT]->(i)",
            person=person,  # => binds $person -- who bought it
            item=item,  # => binds $item -- what they bought
        )  # => idempotent per-edge write


with (
    driver.session() as session
):  # => opens one session for both the load and the verify read
    session.execute_write(
        load
    )  # => runs the whole load() function as one write transaction
    counts = session.execute_read(
        lambda tx: tx.run(
            "MATCH (p:Person) WITH count(p) AS people "  # => counts every Person node just loaded
            "MATCH (i:Item) WITH people, count(i) AS items "  # => counts every Item node just loaded
            "MATCH ()-[k:KNOWS]->() WITH people, items, count(k) AS knows "  # => counts every KNOWS edge
            "MATCH ()-[b:BOUGHT]->() RETURN people, items, knows, count(b) AS bought"
            # => counts every BOUGHT edge, carrying the three prior counts along via WITH
        ).single()
    )  # => a single summary row verifying every count matches the source lists above
    print(dict(counts))  # => {'people': 5, 'items': 3, 'knows': 5, 'bought': 4}

driver.close()  # => releases the driver's connection pool cleanly
