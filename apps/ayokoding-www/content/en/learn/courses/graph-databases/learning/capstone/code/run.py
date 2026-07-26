# Capstone Step 2: run.py -- Run queries.cypher's Two Queries from Python. (co-05, co-08, co-09)
from neo4j import GraphDatabase  # => driver package, `pip install neo4j`

driver = GraphDatabase.driver(
    "bolt://localhost:7687", auth=("neo4j", "password")
)  # => driver handle
# => a live connection -- swap the URI/credentials for your own setup


def neighborhood(
    tx, name: str
) -> list[str]:  # => Query 1 from queries.cypher, run parameterized
    result = tx.run(  # => the neighborhood query call itself
        "MATCH (u:Person {name: $name})-[:BOUGHT]->(i:Item)<-[:BOUGHT]-(other:Person) "
        # => 2-hop pattern: u's purchase, then back OUT to whoever else bought the same item
        "RETURN DISTINCT other.name AS name",
        name=name,  # => binds $name -- the starting person's name
    )  # => end of the neighborhood query call
    return [
        row["name"] for row in result
    ]  # => every OTHER buyer of anything $name bought


def friends_of_friends(
    tx, name: str
) -> list[str]:  # => Query 2 from queries.cypher, run parameterized
    result = tx.run(  # => the bounded-traversal query call itself
        "MATCH (a:Person {name: $name})-[:KNOWS*1..2]-(b:Person) RETURN DISTINCT b.name AS name",
        name=name,  # => binds $name -- the starting person's name
    )  # => end of the bounded-traversal query call
    return sorted(
        row["name"] for row in result
    )  # => sorted for a deterministic, checkable order


with driver.session() as session:  # => opens one session for both reads
    neighbors = session.execute_read(neighborhood, "Ada")  # => Query 1, against Ada
    fof = session.execute_read(friends_of_friends, "Ada")  # => Query 2, against Ada
    print(
        f"Neighborhood (co-buyers of Ada's purchases): {neighbors}"
    )  # => hand-traced in the Verify block
    print(
        f"Friends-of-friends within 2 KNOWS hops: {fof}"
    )  # => hand-traced in the Verify block

driver.close()  # => releases the driver's connection pool cleanly
