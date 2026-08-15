"""Safe local checkpoints for a narrated live-coding rehearsal."""

from __future__ import annotations


class TicketError(ValueError):
    """The tiny live-round ticket violates its stated boundary."""


def first_checkpoint() -> list[str]:
    """Return a runnable minimal slice before parsing or sorting exists."""

    return []


def add_ticket(tickets: list[str], title: str) -> list[str]:
    """Return a new, validated ticket list without mutating the caller's list."""

    cleaned = title.strip()
    if not cleaned:
        raise TicketError("ticket title must not be blank")
    return [*tickets, cleaned]


def visible_titles(tickets: list[str]) -> list[str]:
    """Return deterministic output after the interviewer asks for sorting."""

    return sorted(tickets, key=str.casefold)
