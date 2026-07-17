"""Example 65: pytest verification for Actor Mailbox."""

from example import CounterActor


def test_messages_handled_in_arrival_order() -> None:
    actor = CounterActor()  # => fresh actor, isolated from the module-level demo
    actor.send("increment")
    actor.send("decrement")
    actor.send("increment")
    actor.process_all()
    assert actor.handled_order == ["increment", "decrement", "increment"]  # => exact arrival order preserved


def test_sending_alone_never_mutates_state() -> None:
    actor = CounterActor()  # => fresh actor
    actor.send("increment")  # => enqueue only
    actor.send("increment")  # => enqueue only
    assert actor.read_count() == 0  # => count untouched until process_one/process_all actually runs


def test_final_count_matches_the_net_effect_of_all_messages() -> None:
    actor = CounterActor()  # => fresh actor
    for message in ["increment", "increment", "increment", "decrement"]:
        actor.send(message)
    actor.process_all()
    assert actor.read_count() == 2  # => +1+1+1-1


# => Run: pytest -- Output: 3 passed
