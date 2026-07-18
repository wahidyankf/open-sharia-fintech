# pyright: strict
"""Kata 1 (after): a None default plus a fresh list built INSIDE __init__ gives every
instance its OWN wheres list -- nothing leaks across instances anymore (co-03)."""


class Builder:
    def __init__(self, table: str, wheres: list[str] | None = None) -> None:  # THE FIX: None, not []
        self.table = table
        self.wheres = wheres if wheres is not None else []  # a FRESH list, built fresh on EVERY call

    def where(self, clause: str) -> "Builder":
        self.wheres.append(clause)  # mutates THIS instance's own list, never a shared one
        return self

    def compile(self) -> str:
        if self.wheres:
            return f"SELECT * FROM {self.table} WHERE {' AND '.join(self.wheres)}"
        return f"SELECT * FROM {self.table}"


b1 = Builder("customer").where("id = 1")
b2 = Builder("orders")  # gets its OWN empty list -- b1's clause cannot possibly reach it
print(b1.compile())
print(b2.compile())
