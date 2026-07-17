"""Example 48: pytest verification for the Mediator Decoupling Two Collaborators."""

from example import ChatRoom, Participant


def test_message_is_delivered_through_the_mediator() -> None:
    room: ChatRoom = ChatRoom()
    alice: Participant = Participant("alice", room)
    bob: Participant = Participant("bob", room)
    room.register(alice)
    room.register(bob)
    alice.send("bob", "hello")
    assert bob.inbox == ["alice: hello"]  # => delivered despite no direct reference


def test_neither_participant_holds_a_reference_to_the_other() -> None:
    room: ChatRoom = ChatRoom()
    alice: Participant = Participant("alice", room)
    bob: Participant = Participant("bob", room)
    assert "bob" not in vars(alice).values()  # => alice's own attributes never name bob
    assert "alice" not in vars(bob).values()  # => bob's own attributes never name alice


# => Run: pytest -- Output: 2 passed
