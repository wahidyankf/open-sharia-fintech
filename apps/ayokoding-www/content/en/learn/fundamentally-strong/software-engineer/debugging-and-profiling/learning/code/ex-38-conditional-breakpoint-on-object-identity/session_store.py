"""Example 38: A Conditional Breakpoint on Object Identity."""

from __future__ import annotations


class Session:
    def __init__(self, user: str) -> None:
        self.user = user


def touch(session: Session) -> None:
    session.user = (
        session.user
    )  # a stop point -- but only interesting for ONE specific instance


if __name__ == "__main__":
    sessions = [Session("alice"), Session("bob"), Session("carol")]
    target = sessions[1]  # the ONE instance this example wants to catch, by identity
    print("target id:", id(target))
    for s in sessions:
        touch(s)
    print("done")
