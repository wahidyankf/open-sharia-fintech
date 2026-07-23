"""Example 10: .join() Adds a JOIN Fragment With an ON Predicate."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => dataclasses.replace() is the immutable "update" primitive
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass(frozen=True)  # => co-03: immutable, one method per fluent step
class Select:  # => same shape as Examples 7-9, now grows a JOIN fragment
    columns: tuple[str, ...] = ()  # => the SELECT list
    table: str | None = None  # => FROM target
    joins: tuple[str, ...] = ()  # => accumulated "JOIN t ON pred" fragments, in order

    def from_(self, table: str) -> "Select":  # => attaches the FROM target
        return dataclasses.replace(self, table=table)  # => new instance, table now set

    def join(self, table: str, on: str) -> "Select":  # => co-04: appends one JOIN fragment
        fragment = f"JOIN {table} ON {on}"  # => "JOIN orders ON users.id = orders.user_id"
        return dataclasses.replace(self, joins=self.joins + (fragment,))  # => new joins tuple

    def compile(self) -> str:  # => assembles SELECT, FROM, and every JOIN fragment
        col_list = ", ".join(self.columns) if self.columns else "*"  # => join or fall back
        sql = f"SELECT {col_list} FROM {self.table}"  # => base SELECT ... FROM
        if self.joins:  # => append JOIN fragments only if at least one was added
            sql += " " + " ".join(self.joins)  # => space-joined, in the order they were added
        return sql  # => the final assembled SQL string


def select(*columns: str) -> Select:  # => the public entry point
    return Select(columns=columns)  # => columns arrive as a tuple, in call order


query = (  # => a three-step fluent chain, each step returning a new immutable Select
    select("users.name", "orders.total")  # => two columns from two different tables
    .from_("users")  # => the driving table
    .join("orders", on="users.id = orders.user_id")  # => the JOIN this example is about
)  # => query now holds the fully-chained, still-uncompiled builder state
sql = query.compile()  # => renders the accumulated state to SQL text
assert "JOIN orders ON users.id = orders.user_id" in sql  # => the exact JOIN fragment appears

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => parent table
    conn.execute("CREATE TABLE orders(user_id INTEGER, total REAL)")  # => child table
    conn.execute("INSERT INTO users(id, name) VALUES (1, 'Alice')")  # => one user
    conn.execute("INSERT INTO orders(user_id, total) VALUES (1, 42.5)")  # => one matching order
    conn.commit()  # => makes both seed rows visible
    row = conn.execute(sql).fetchone()  # => runs the compiled JOIN for real
    print(row)  # => Output: ('Alice', 42.5)
    # => proves the JOIN fragment matched Alice's user row to her order row correctly
