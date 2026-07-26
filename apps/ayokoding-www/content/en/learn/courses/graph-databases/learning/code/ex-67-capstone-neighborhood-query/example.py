# Example 67: Preview: a Neighborhood Query from Python. (co-05, co-08)
from neo4j import GraphDatabase  # => driver package, `pip install neo4j`

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
# => a live connection -- swap the URI/credentials for your own setup


def seed(
    tx,
) -> None:  # => plants the small shared-purchase fixture this example queries
    tx.run(
        "CREATE (:User {name: 'Ada'})-[:BOUGHT]->(:Item {name: 'Keyboard'})"  # => Ada's purchase
        "<-[:BOUGHT]-(:User {name: 'Bob'})"  # => Bob's purchase of the SAME item, chained on
    )  # => Ada and Bob share exactly one purchased item -- a small, hand-checkable neighborhood


def neighborhood(tx, name: str) -> list[str]:  # => the query under test in this example
    # co-05, co-08: 1-hop direct purchases, plus 2-hop "who else bought the same thing."
    result = tx.run(  # => the neighborhood query call itself
        "MATCH (u:User {name: $name})-[:BOUGHT]->(i:Item)<-[:BOUGHT]-(other:User) "
        # => 2-hop pattern: u's purchase, then back OUT to whoever else bought the same item
        "RETURN DISTINCT other.name AS name",  # => DISTINCT avoids duplicate rows per shared item
        name=name,  # => binds $name -- the starting user's name
    )  # => end of the neighborhood query call
    return [
        row["name"] for row in result
    ]  # => co-buyers of anything Ada bought, excluding Ada


with (
    driver.session() as session
):  # => opens one session for both the seed write and the read
    session.execute_write(seed)  # => runs seed() as one write transaction
    result = session.execute_read(
        neighborhood, "Ada"
    )  # => runs neighborhood() as one read
    print(
        result
    )  # => hand-checked: Bob is Ada's only 2-hop co-buyer neighbor in this fixture

driver.close()  # => releases the driver's connection pool cleanly
