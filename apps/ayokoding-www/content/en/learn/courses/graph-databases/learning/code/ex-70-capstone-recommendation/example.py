# Example 70: Preview: a Recommendation Query from Python. (co-15)
from neo4j import GraphDatabase  # => driver package, `pip install neo4j`

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
# => a live connection -- swap the URI/credentials for your own setup


def seed(
    tx,
) -> None:  # => plants Ada's one purchase, plus Bob's overlapping + extra purchase
    tx.run(  # => call 1: Ada's single purchase
        "CREATE (:User {name: 'Ada'})-[:BOUGHT]->(:Item {name: 'Keyboard'})"  # => Ada's only buy
    )  # => end of call 1
    tx.run(  # => call 2: Bob's two purchases, in a SEPARATE transaction call
        "MATCH (i:Item {name: 'Keyboard'}) "  # => finds the SAME Keyboard node call 1 just created
        "CREATE (o:User {name: 'Bob'})-[:BOUGHT]->(i) "  # => shares that SAME node, not a namesake
        "CREATE (o)-[:BOUGHT]->(:Item {name: 'Mousepad'})"  # => Bob's EXTRA purchase, the candidate
    )  # => same co-occurrence shape as Example 39 -- Bob shares Keyboard, ALSO bought Mousepad


def recommend(
    tx, name: str
) -> list[str]:  # => the ranked co-occurrence query under test
    result = tx.run(  # => the recommendation query call itself
        "MATCH (u:User {name: $name})-[:BOUGHT]->(:Item)<-[:BOUGHT]-(other)-[:BOUGHT]->(rec:Item) "
        # => 3-hop co-occurrence chain, identical shape to Example 39's Cypher-only version
        "WHERE NOT (u)-[:BOUGHT]->(rec) "  # => excludes anything the user already owns
        "RETURN rec.name AS name, count(*) AS score ORDER BY score DESC",  # => ranked by co-buyer count
        name=name,  # => binds $name -- the starting user's name
    )  # => end of the recommendation query call
    return [
        row["name"] for row in result
    ]  # => co-15: ranked recommendation list, highest score first


with (
    driver.session() as session
):  # => opens one session for both the seed write and the read
    session.execute_write(seed)  # => runs seed() as one write transaction
    result = session.execute_read(
        recommend, "Ada"
    )  # => runs recommend() as one read transaction
    print(
        result
    )  # => hand-checked: Mousepad is Ada's one and only reproducible recommendation

driver.close()  # => releases the driver's connection pool cleanly
