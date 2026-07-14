from collections.abc import Callable


class Connection:  # => stands in for a real DB connection object
    def __init__(self, name: str) -> None:
        self.name = name
        self.closed = False

    def close(self) -> None:
        self.closed = True


def get_connection(pool: list[Connection]) -> Connection:  # => co-23: a FastAPI-Depends-style PROVIDER
    return pool.pop()  # => hands out ONE connection per call, taking it out of the shared pool


def run_with_dependency(  # => co-23: mimics what FastAPI does with `Depends(get_connection)` per request
    provider: Callable[[], Connection], handler: Callable[[Connection], str]
) -> str:
    connection = provider()  # => co-23: the FRAMEWORK resolves the dependency -- the handler never calls it
    try:
        return handler(connection)  # => co-23: the handler just RECEIVES a ready-to-use resource
    finally:
        connection.close()  # => co-23: the framework is responsible for teardown too, not the handler


def list_tasks_handler(connection: Connection) -> str:  # => co-08: a thin handler -- no wiring logic itself
    return f"tasks from {connection.name}"


pool = [Connection("conn-a"), Connection("conn-b")]  # => co-23: a mocked connection pool
provider = lambda: get_connection(pool)  # => co-23: bound once, reused per simulated "request"

result = run_with_dependency(provider, list_tasks_handler)  # => request 1: injected with conn-b (last popped)
print(result)  # => Output: tasks from conn-b
print(len(pool))  # => Output: 1 -- whatever's left in the pool after one injection

assert result == "tasks from conn-b"
assert len(pool) == 1  # => co-23: exactly one connection was handed out and consumed
print("kata-18 OK")
