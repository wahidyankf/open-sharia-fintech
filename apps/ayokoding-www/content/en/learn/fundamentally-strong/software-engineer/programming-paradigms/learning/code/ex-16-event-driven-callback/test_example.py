"""Example 16: pytest verification for Event-Driven Callback."""

from example import Dispatcher


def test_handler_runs_with_the_fired_payload() -> None:
    dispatcher = Dispatcher()  # => fresh dispatcher, isolated from the module-level demo
    seen: list[dict[str, str]] = []  # => local recorder for this test only
    dispatcher.on("ping", lambda payload: seen.append(payload))  # => register a lambda handler
    dispatcher.fire("ping", {"id": "42"})  # => trigger the event
    assert seen == [{"id": "42"}]  # => the handler ran exactly once, with the exact payload


def test_registering_alone_never_runs_the_handler() -> None:
    dispatcher = Dispatcher()  # => fresh dispatcher
    seen: list[dict[str, str]] = []  # => local recorder
    dispatcher.on("ping", lambda payload: seen.append(payload))  # => register only, never fire
    assert seen == []  # => registration is inert until fire() is called


# => Run: pytest -- Output: 2 passed
