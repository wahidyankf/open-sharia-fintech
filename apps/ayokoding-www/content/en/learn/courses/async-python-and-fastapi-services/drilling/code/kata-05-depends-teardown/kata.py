"""Kata 5 -- A Depends-style provider with teardown (co-15)."""

from collections.abc import Iterator  # => the shape of a yield-provider (co-15)


class Conn:  # => a stand-in resource
    def __init__(self, name: str) -> None:
        self.name = name
        self.closed = False

    def close(self) -> None:  # => teardown
        self.closed = True


def run_with_dependency(  # => mimics what Depends does per request (co-15)
    provider: Iterator[Conn],
    handler,
) -> str:
    resource = next(provider)  # => resolve the resource (the part before yield)
    try:
        return handler(resource)  # => the handler just RECEIVES the resource
    finally:
        try:  # => always run teardown, even on error
            next(provider)  # => drive the provider past yield -> runs its teardown
        except StopIteration:  # => the generator finished -- expected after teardown
            pass


def get_conn() -> Iterator[Conn]:  # => a yield-provider (co-15)
    conn = Conn("primary")  # => setup
    yield conn  # => hand it out
    conn.close()  # => teardown -- runs after the handler returns/raises


def use_conn(c: Conn) -> str:  # => a handler that just uses the resource
    return f"used {c.name}"


def main() -> None:
    result = run_with_dependency(get_conn(), use_conn)  # => provider + handler
    print(result)  # => Output: used primary
    assert result == "used primary"


if __name__ == "__main__":
    main()
