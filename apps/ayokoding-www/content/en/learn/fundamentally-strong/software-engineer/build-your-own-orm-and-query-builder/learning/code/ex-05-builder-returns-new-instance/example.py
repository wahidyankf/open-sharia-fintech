"""Example 5: A Builder Method Returns a NEW Instance, Never Mutates."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => dataclasses.replace() is the immutable "update" primitive
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass(frozen=True)  # => frozen: attribute assignment raises, by design
class Query:  # => co-03: an immutable fluent builder over a single table
    table: str  # => which table this query targets
    wheres: tuple[str, ...] = ()  # => accumulated raw WHERE fragments, empty by default

    def where(self, clause: str) -> "Query":  # => returns a NEW Query, self is untouched
        return dataclasses.replace(  # => copies every field, overriding only wheres
            self,
            wheres=self.wheres + (clause,),  # => appends clause to a NEW tuple
        )

    def compile(self) -> str:  # => turns the accumulated fragments into one SQL string
        sql = f"SELECT * FROM {self.table}"  # => base SELECT, no WHERE yet
        if self.wheres:  # => only append WHERE if at least one fragment was added
            sql += " WHERE " + " AND ".join(self.wheres)  # => joins fragments with AND
        return sql  # => the final, fully-assembled SQL string for this instance


base = Query(table="users")  # => the original, zero-filter query
filtered = base.where("age > 18")  # => calling .where() on base...
# => ...returns a DIFFERENT object -- base itself is never touched
assert base.wheres == ()  # => base still has NO filters -- proves immutability
assert filtered.wheres == ("age > 18",)  # => only the NEW object carries the filter
assert base is not filtered  # => two distinct objects, not the same instance mutated
assert base.compile() == "SELECT * FROM users"  # => base's SQL never gained a WHERE

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, age INTEGER)")  # => real table
    conn.execute("INSERT INTO users(id, age) VALUES (1, 15), (2, 25)")  # => two seed rows
    conn.commit()  # => makes both seed rows visible
    base_rows = conn.execute(base.compile()).fetchall()  # => runs base's unfiltered SQL
    filtered_rows = conn.execute(filtered.compile()).fetchall()  # => runs filtered's SQL
    print(len(base_rows), len(filtered_rows))  # => Output: 2 1
    # => base still sees both rows; filtered sees only the one row over 18
