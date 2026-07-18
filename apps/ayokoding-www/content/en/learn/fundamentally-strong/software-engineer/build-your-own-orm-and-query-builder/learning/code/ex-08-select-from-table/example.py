"""Example 8: .from_() Attaches the FROM Target, Immutably."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => dataclasses.replace() is the immutable "update" primitive
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass(frozen=True)  # => co-03: immutable, one method per fluent step
class Select:  # => same shape as Example 7, focus shifted onto .from_() itself
    columns: tuple[str, ...] = ()  # => the SELECT list
    table: str | None = None  # => FROM target -- None until .from_() is called

    def from_(self, table: str) -> "Select":  # => the method THIS example is about
        return dataclasses.replace(self, table=table)  # => new instance, table now set

    def compile(self) -> str:  # => assembles the SELECT clause from state
        col_list = ", ".join(self.columns) if self.columns else "*"  # => join or fall back
        return f"SELECT {col_list} FROM {self.table}"  # => the final assembled SQL string


def select(*columns: str) -> Select:  # => the public entry point
    return Select(columns=columns)  # => columns arrive as a tuple, in call order


before = select("id")  # => built, but .from_() has not run yet
assert before.table is None  # => no FROM target attached yet -- state is inspectable
after = before.from_("orders")  # => attaches "orders" as the FROM target
assert before.table is None  # => the ORIGINAL object is still untouched -- immutability
assert after.table == "orders"  # => only the NEW object carries "orders"
assert after.compile() == "SELECT id FROM orders"  # => FROM orders now appears in the SQL

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, total REAL)")  # => real table
    conn.execute("INSERT INTO orders(id, total) VALUES (1, 42.5)")  # => one seed row
    conn.commit()  # => makes the seed row visible to the SELECT below
    row = conn.execute(after.compile()).fetchone()  # => runs against the real "orders" table
    print(row)  # => Output: (1,)
    # => proves .from_("orders") pointed the query at the correct real table
