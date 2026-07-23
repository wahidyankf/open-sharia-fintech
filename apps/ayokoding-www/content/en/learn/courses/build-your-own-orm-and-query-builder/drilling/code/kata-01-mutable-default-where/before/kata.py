# pyright: strict
"""Kata 1 (before): a mutable default argument makes a "builder" leak WHERE clauses
across EVERY instance that never explicitly passes its own list (co-03)."""


class Builder:
    def __init__(self, table: str, wheres: list[str] = []) -> None:  # BUG: the SAME list, shared forever
        self.table = table
        self.wheres = wheres  # not copied -- aliases the ONE default list object every call re-uses

    def where(self, clause: str) -> "Builder":
        self.wheres.append(clause)  # mutates the SHARED default list, not a per-instance one
        return self

    def compile(self) -> str:
        if self.wheres:
            return f"SELECT * FROM {self.table} WHERE {' AND '.join(self.wheres)}"
        return f"SELECT * FROM {self.table}"


# intent: b2 never calls .where() at all -- it should compile to a plain, unfiltered SELECT.
b1 = Builder("customer").where("id = 1")
b2 = Builder("orders")
print(b1.compile())
print(b2.compile())
