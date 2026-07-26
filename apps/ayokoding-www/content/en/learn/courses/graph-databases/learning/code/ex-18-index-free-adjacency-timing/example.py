# Example 18: Index-Free Adjacency Keeps a Hop Cheap. (co-04)
# This is a real, runnable neo4j Python-driver script -- against a live Neo4j instance it builds a
# small graph, times a 1-hop expansion, then builds a much larger one and times the SAME expansion.
from neo4j import GraphDatabase  # => driver package, `pip install neo4j`
import time  # => stdlib, used only for perf_counter() timing below

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
# => connects to a local Neo4j instance -- swap the URI/credentials for your own setup


def build_star_graph(tx, center_label: str, n: int) -> None:
    # A "star": one center node with n outgoing edges -- n controls total graph size,
    # while the center node's OWN degree also grows with n (a deliberately worst-case shape).
    tx.run(
        # a fresh center node, then n leaves each connected directly to it
        f"UNWIND range(1, $n) AS i CREATE (:{center_label})-[:LINK]->(:Leaf {{i: i}})",
        n=n,  # => bound parameter -- never string-interpolated into the query text
    )  # => n new leaves and n new LINK edges, all hanging off ONE freshly created center per call


def time_one_hop(tx, center_label: str) -> float:
    # Times ONE hop out of the named center label -- the operation under comparison.
    start = time.perf_counter()  # => wall-clock start, right before the traversal runs
    tx.run(f"MATCH (c:{center_label})-[:LINK]->(leaf) RETURN count(leaf)").consume()
    # => one-hop expansion from the SAME center node -- the query the timing compares across sizes
    # => .consume() forces the whole result to be pulled server-side before timing stops
    return (
        time.perf_counter() - start
    )  # => elapsed seconds for exactly this one-hop expansion


with driver.session() as session:
    session.execute_write(
        build_star_graph, "SmallCenter", 10
    )  # => small graph: 10 leaves
    session.execute_write(
        build_star_graph, "BigCenter", 10_000
    )  # => large graph: 10,000 leaves
    small_t = session.execute_read(time_one_hop, "SmallCenter")
    # => times a hop from the SMALL center -- degree 10
    big_t = session.execute_read(time_one_hop, "BigCenter")
    # => times a hop from the BIG center -- degree 10,000, a completely different subgraph
    print(f"small (10 leaves):    {small_t:.4f}s")
    # => prints the small-graph timing for visual comparison
    print(f"big   (10,000 leaves): {big_t:.4f}s")
    # => prints the big-graph timing -- see Verify below for what to expect, qualitatively

driver.close()
# => releases the driver's connection pool cleanly
