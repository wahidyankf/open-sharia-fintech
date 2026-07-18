"""Example 6: Branch a Partial Query into Two Independent Variants."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => dataclasses.replace() is the immutable "update" primitive
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass(frozen=True)  # => same immutable shape as Example 5
class Query:  # => an immutable fluent builder over a single table
    table: str  # => target table
    wheres: tuple[str, ...] = ()  # => accumulated WHERE fragments

    def where(self, clause: str) -> "Query":  # => branch point -- returns a new Query
        return dataclasses.replace(self, wheres=self.wheres + (clause,))  # => new tuple, new object

    def compile(self) -> str:  # => turns fragments into one SELECT string
        sql = f"SELECT * FROM {self.table}"  # => base SELECT, no WHERE yet
        if self.wheres:  # => only append WHERE if at least one fragment was added
            sql += " WHERE " + " AND ".join(self.wheres)  # => joins fragments with AND
        return sql  # => the final, fully-assembled SQL string for this instance


base = Query(table="orders").where("region = 'west'")  # => ONE shared partial query
# => base already carries one filter -- this is the reusable "trunk" both branches share
variant_open = base.where("status = 'open'")  # => BRANCH 1: adds an open-status filter
variant_closed = base.where("status = 'closed'")  # => BRANCH 2: adds a closed-status filter
# => both branches started from the SAME base -- neither one touched the other

assert base.wheres == ("region = 'west'",)  # => the shared trunk still has only ITS filter
assert variant_open.wheres == ("region = 'west'", "status = 'open'")  # => trunk + open
assert variant_closed.wheres == ("region = 'west'", "status = 'closed'")  # => trunk + closed
assert variant_open is not variant_closed  # => two distinct objects, no cross-contamination

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, region TEXT, status TEXT)")  # => table
    conn.execute(  # => three seed rows across two regions and two statuses
        "INSERT INTO orders(id, region, status) VALUES "  # => column list, VALUES keyword
        "(1, 'west', 'open'), (2, 'west', 'closed'), (3, 'east', 'open')"  # => three literal rows
    )
    conn.commit()  # => makes all three seed rows visible
    open_rows = conn.execute(variant_open.compile()).fetchall()  # => runs branch 1's SQL
    closed_rows = conn.execute(variant_closed.compile()).fetchall()  # => runs branch 2's SQL
    print(len(open_rows), len(closed_rows))  # => Output: 1 1
    # => each branch independently filters west-region rows down to its own status
