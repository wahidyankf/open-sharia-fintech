# Capstone Step 3: recommend.py -- a Recommendation Query and a Shortest-Path Query. (co-10, co-15)
from neo4j import GraphDatabase  # => driver package, `pip install neo4j`

driver = GraphDatabase.driver(
    "bolt://localhost:7687", auth=("neo4j", "password")
)  # => driver handle
# => a live connection -- swap the URI/credentials for your own setup


def recommend(
    tx, name: str
) -> list[str]:  # => co-15: "people who bought X also bought Y"
    result = tx.run(
        "MATCH (u:Person {name: $name})-[:BOUGHT]->(:Item)<-[:BOUGHT]-(other)-[:BOUGHT]->(rec:Item) "
        # => 3-hop co-occurrence chain: u's purchase, a co-buyer, that co-buyer's OTHER purchase
        "WHERE NOT (u)-[:BOUGHT]->(rec) "  # => excludes anything the user already owns
        "RETURN rec.name AS name, count(*) AS score ORDER BY score DESC",  # => ranked by co-buyer count
        name=name,  # => binds $name -- the starting person's name
    )  # => end of the recommendation query call
    return [
        row["name"] for row in result
    ]  # => co-15: ranked recommendation list, highest score first


def shortest_hops(
    tx, a_name: str, z_name: str
) -> int:  # => co-10: the shortestPath() query under test
    result = tx.run(
        "MATCH (a:Person {name: $a}), (z:Person {name: $z}) "  # => binds both named endpoints
        "MATCH p = shortestPath((a)-[:KNOWS*]-(z)) RETURN length(p) AS hops",
        a=a_name,  # => binds $a -- the source person's name
        z=z_name,  # => binds $z -- the target person's name
    )  # => end of the shortest-path query call
    return result.single()["hops"]  # => co-10: the SHORTEST path's hop count


with driver.session() as session:  # => opens one session for both reads
    recs = session.execute_read(recommend, "Ada")  # => runs recommend() against Ada
    hops = session.execute_read(
        shortest_hops, "Ada", "Dee"
    )  # => runs shortest_hops() from Ada to Dee
    print(f"Recommendation for Ada: {recs}")  # => hand-traced in the Verify block
    print(
        f"Shortest KNOWS path, Ada to Dee: {hops} hops"
    )  # => hand-traced in the Verify block

driver.close()  # => releases the driver's connection pool cleanly
