# Example 69: Preview: Shortest Path from Python. (co-10)
from neo4j import GraphDatabase  # => driver package, `pip install neo4j`

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
# => a live connection -- swap the URI/credentials for your own setup


def seed(
    tx,
) -> None:  # => plants BOTH a 2-hop chain and a 1-hop shortcut between Ada and Zoe
    tx.run(  # => call 1: plants the 2-hop chain
        "CREATE (:Person {name: 'Ada'})-[:KNOWS]->(:Person {name: 'Bob'})"  # => hop 1: Ada->Bob
        "-[:KNOWS]->(:Person {name: 'Zoe'})"  # => hop 2: Bob->Zoe, the LONGER 2-hop route
    )  # => end of call 1
    tx.run(  # => call 2: plants the direct shortcut, in a SEPARATE transaction call
        "MATCH (a:Person {name: 'Ada'}), (z:Person {name: 'Zoe'}) CREATE (a)-[:KNOWS]->(z)"
    )  # => a DIRECT 1-hop shortcut also exists, exactly like Example 16's fixture


def shortest_hops(
    tx, a_name: str, z_name: str
) -> int:  # => the shortestPath() query under test
    result = tx.run(  # => the shortest-path query call itself
        "MATCH (a:Person {name: $a}), (z:Person {name: $z}) "  # => binds both named endpoints
        "MATCH p = shortestPath((a)-[:KNOWS*]-(z)) RETURN length(p) AS hops",
        # => a SECOND MATCH clause -- shortestPath() needs both endpoints already bound
        a=a_name,  # => binds $a -- the source person's name
        z=z_name,  # => binds $z -- the target person's name
    )  # => end of the shortest-path query call
    return result.single()["hops"]  # => co-10: the SHORTEST path's hop count


with (
    driver.session() as session
):  # => opens one session for both the seed write and the read
    session.execute_write(seed)  # => runs seed() as one write transaction
    hops = session.execute_read(
        shortest_hops, "Ada", "Zoe"
    )  # => runs shortest_hops() as one read
    print(
        hops
    )  # => hand-traced: the direct 1-hop shortcut beats the 2-hop detour, matching Example 16

driver.close()  # => releases the driver's connection pool cleanly
