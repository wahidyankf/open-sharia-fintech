# Example 44: Supernode Traversal Cost. (co-17, co-04)
from neo4j import GraphDatabase  # => driver package, `pip install neo4j`
import time  # => stdlib, used only for perf_counter() timing below

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
# => a live connection -- swap the URI/credentials for your own setup


def build_fixture(tx) -> None:
    # Builds TWO separate subgraphs: an ordinary degree-1 node and a deliberately extreme
    # degree-50,000 supernode -- the two shapes this example's timing compares.
    tx.run(
        "CREATE CONSTRAINT person_name_unique IF NOT EXISTS "
        "FOR (p:Person) REQUIRE p.name IS UNIQUE"
    )
    # => an index-backed uniqueness constraint on Person.name, created BEFORE any Person node exists
    # -- without it, time_expand's MATCH (p:Person {name: $name}) pays an unindexed label scan across
    # every Person node (50,003 of them once the fixture below finishes), which swamps the
    # degree-driven expand cost this example is trying to isolate
    tx.run(
        "CREATE (:Person {name: 'Ordinary'})-[:KNOWS]->(:Person {name: 'OneFriend'})"
    )
    # => degree-1 node: exactly ONE relationship to expand through
    tx.run(
        # a single Cypher statement, string-built here for readability, run as ONE query
        "CREATE (hub:Person {name: 'Hub'}) "
        "WITH hub UNWIND range(1, 50000) AS i "
        "CREATE (hub)-[:KNOWS]->(:Person {name: 'L' + toString(i)})"
        # => WITH hub carries the alias into UNWIND, exactly like Example 43's fix
    )  # => degree-50,000 SUPERNODE -- deliberately extreme, to make the cost gap visible


def time_expand(tx, name: str) -> float:
    # Times a full 1-hop expansion out of the named node -- the operation under comparison.
    start = (
        time.perf_counter()
    )  # => wall-clock start, right before the expansion query runs
    tx.run(
        "MATCH (p:Person {name: $name})-[:KNOWS]->(x) RETURN count(x)", name=name
    ).consume()
    # => expands EVERY relationship the named node has -- the operation under comparison
    # => .consume() forces the whole result to be pulled server-side before timing stops
    return (
        time.perf_counter() - start
    )  # => elapsed seconds for exactly this one-hop expansion


with driver.session() as session:
    session.execute_write(
        build_fixture
    )  # => runs the constraint + both CREATE statements above, once
    ordinary_t = session.execute_read(time_expand, "Ordinary")  # => degree-1 expansion
    hub_t = session.execute_read(time_expand, "Hub")  # => degree-50,000 expansion
    print(f"ordinary (degree 1):    {ordinary_t:.4f}s")
    # => prints the small-degree timing for visual comparison
    print(f"hub      (degree 50000): {hub_t:.4f}s")
    # => prints the supernode timing -- see Verify below for what to expect, qualitatively

driver.close()
# => releases the driver's connection pool cleanly
