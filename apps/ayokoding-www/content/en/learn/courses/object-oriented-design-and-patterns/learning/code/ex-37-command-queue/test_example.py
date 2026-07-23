"""Example 37: pytest verification for Queueing Commands for Deferred Batch Execution."""

from example import CommandQueue, LogEventCommand, SendEmailCommand


def test_run_all_executes_commands_in_enqueue_order() -> None:
    queue: CommandQueue = CommandQueue()
    queue.enqueue(LogEventCommand("first"))
    queue.enqueue(SendEmailCommand("second@example.com"))
    queue.enqueue(LogEventCommand("third"))
    results: list[str] = queue.run_all()
    assert results == [
        "logged: first",
        "email sent to second@example.com",
        "logged: third",
    ]  # => exact enqueue order preserved


def test_run_all_empties_the_queue() -> None:
    queue: CommandQueue = CommandQueue()
    queue.enqueue(LogEventCommand("only"))
    queue.run_all()
    assert queue._pending == []  # => nothing left pending after a batch has run


# => Run: pytest -- Output: 2 passed
