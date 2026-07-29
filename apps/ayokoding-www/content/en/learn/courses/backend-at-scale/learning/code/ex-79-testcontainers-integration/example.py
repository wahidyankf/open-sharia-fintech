# pyright: strict
"""Example 79: Testcontainers -- an integration test against a real engine. (co-36)

Testcontainers spins up EPHEMERAL, lightweight Docker container instances of
real dependencies (a DB, a broker) for automated tests, instead of mocks.
This example simulates the lifecycle: a fresh isolated engine instance per
test, a REAL query against it, then teardown. Source: testcontainers.com.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-36: an ephemeral containerized DB instance (stands in for a real Docker container)
class ContainerDB:
    container_id: int  # => a unique id for this ephemeral instance
    rows: dict[int, str] = field(default_factory=dict[int, str])  # => the engine's own isolated state
    running: bool = True  # => the container is up until torn down

    def query(self, key: int) -> str | None:  # => a REAL query against the (simulated) engine
        if not self.running:  # => the container was torn down
            raise RuntimeError("container stopped")  # => cannot query a stopped container
        return self.rows.get(key)  # => the engine's real answer

    def insert(self, key: int, value: str) -> None:  # => a REAL write against the engine
        if not self.running:  # => the container was torn down
            raise RuntimeError("container stopped")  # => cannot write to a stopped container
        self.rows[key] = value  # => the engine persists it

    def stop(self) -> None:  # => co-36: teardown -- the ephemeral instance is destroyed
        self.running = False  # => the container is gone (its state does not leak to the next test)


class TestcontainersFactory:  # => co-36: stands in for the testcontainers library
    def __init__(self) -> None:
        self.next_id = 1  # => unique container ids
        self.started: list[int] = []  # => ids of containers started this run

    def start_db(self) -> ContainerDB:  # => co-36: spin up a FRESH, isolated DB instance
        container = ContainerDB(container_id=self.next_id)  # => a brand-new ephemeral instance
        self.started.append(container.container_id)  # => record it
        self.next_id += 1  # => advance
        return container  # => hand the test an isolated engine


factory = TestcontainersFactory()  # => co-36: the library stand-in

# Test 1: a fresh container, real insert + real query, then teardown.
db1 = factory.start_db()  # => co-36: an isolated instance
db1.insert(1, "row-one")  # => a REAL write against the engine
read1 = db1.query(1)  # => a REAL query against the engine
db1.stop()  # => co-36: teardown -- this instance is gone
print(f"test 1 (container {db1.container_id}): wrote 'row-one', read back {read1!r}")  # => Output: real round-trip

# Test 2: a SECOND fresh container -- its state is isolated from test 1 (no leak).
db2 = factory.start_db()  # => co-36: a NEW isolated instance
leaked = db2.query(1)  # => test 1's row is NOT here -- each container starts empty
print(f"test 2 (container {db2.container_id}): test 1's row leaked? {leaked!r}")  # => Output: None (isolated)
db2.stop()  # => teardown

assert read1 == "row-one"  # => co-36: the suite ran a real query against a real engine
assert leaked is None  # => co-36: each container is ephemeral and isolated (no cross-test leak)
assert factory.started == [1, 2]  # => co-36: two distinct ephemeral containers were spun up
