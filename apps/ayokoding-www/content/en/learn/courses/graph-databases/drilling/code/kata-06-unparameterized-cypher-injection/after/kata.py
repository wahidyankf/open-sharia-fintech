# pyright: strict
"""Kata 6 (after): a parameterized query neutralizes the same injection attempt."""

from neo4j import GraphDatabase, Driver  # => driver package, `pip install neo4j`


def find_person_by_name(driver: Driver, name: str) -> list[str]:
    # THE FIX: $name is a placeholder, not a splice point -- the driver binds it
    # as a single opaque value, so it can never change the shape of the query.
    query = "MATCH (p:Person) WHERE p.name = $name RETURN p.name AS name"
    with driver.session() as session:
        result = session.run(query, name=name)
        return [row["name"] for row in result]


driver: Driver = GraphDatabase.driver(
    "bolt://localhost:7687", auth=("neo4j", "password")
)
with driver.session() as session:
    session.run("CREATE (:Person {name: 'Ada'})")
    session.run("CREATE (:Person {name: 'Grace'})")

malicious_input: str = "nobody' OR '1'='1"
print(find_person_by_name(driver, malicious_input))
driver.close()
