import pytest
from checkpoints import TicketError, add_ticket, first_checkpoint, visible_titles


def test_minimal_slice_runs_before_features() -> None:
    assert first_checkpoint() == []


def test_add_ticket_is_immutable_and_validated() -> None:
    original = first_checkpoint()

    assert add_ticket(original, "Review brief") == ["Review brief"]
    assert original == []
    with pytest.raises(TicketError, match="must not be blank"):
        add_ticket(original, "   ")


def test_interviewer_steer_adds_deterministic_sorting() -> None:
    tickets = add_ticket(add_ticket(first_checkpoint(), "zebra"), "Ada")

    assert visible_titles(tickets) == ["Ada", "zebra"]
