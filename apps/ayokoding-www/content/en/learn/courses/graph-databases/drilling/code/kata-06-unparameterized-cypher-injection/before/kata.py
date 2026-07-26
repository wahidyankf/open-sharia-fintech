# pyright: strict
"""Kata 6 (before): a WHERE clause built via string interpolation -- injectable."""

from neo4j import GraphDatabase, Driver  # => driver package, `pip install neo4j`


def find_person_by_name(driver: Driver, name: str) -> list[str]:
    # THE BUG: f-string interpolation lets the caller's input become CYPHER SYNTAX,
    # not just a value -- the query text itself changes shape based on input.
    query = f"MATCH (p:Person) WHERE p.name = '{name}' RETURN p.name AS name"
    with driver.session() as session:
        result = session.run(query)
        return [row["name"] for row in result]


driver: Driver = GraphDatabase.driver(
    "bolt://localhost:7687", auth=("neo4j", "password")
)
# => a live connection -- swap the URI/credentials for your own setup
with driver.session() as session:
    session.run("CREATE (:Person {name: 'Ada'})")
    session.run("CREATE (:Person {name: 'Grace'})")

# a crafted search value: no person is actually named this, but the OR clause
# it injects makes the WHERE condition true for every row in the database.
malicious_input: str = "nobody' OR '1'='1"
print(find_person_by_name(driver, malicious_input))
driver.close()
