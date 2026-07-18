"""Example 9: select() With No Columns Defaults to SELECT *."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => dataclasses.replace() is the immutable "update" primitive
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass(frozen=True)  # => co-03: immutable, one method per fluent step
class Select:  # => same shape as Examples 7-8, focus on the EMPTY-columns default
    columns: tuple[str, ...] = ()  # => empty tuple is the "no columns chosen" signal
    table: str | None = None  # => FROM target

    def from_(self, table: str) -> "Select":  # => attaches the FROM target
        return dataclasses.replace(self, table=table)  # => new instance, table now set

    def compile(self) -> str:  # => co-04: the empty-columns branch lives HERE
        col_list = ", ".join(self.columns) if self.columns else "*"  # => "*" when empty
        # => an empty tuple is falsy in Python -- `if self.columns` catches it directly
        return f"SELECT {col_list} FROM {self.table}"  # => the final assembled SQL string


def select(*columns: str) -> Select:  # => called with ZERO arguments in this example
    return Select(columns=columns)  # => columns is () when select() takes no arguments


query = select().from_("users")  # => no column names supplied at all
assert query.columns == ()  # => the tuple really is empty -- nothing was chosen
assert query.compile() == "SELECT * FROM users"  # => empty columns renders as bare "*"

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
    conn.execute("INSERT INTO users(id, name) VALUES (1, 'Alice')")  # => one seed row
    conn.commit()  # => makes the seed row visible to the SELECT below
    row = conn.execute(query.compile()).fetchone()  # => runs the real "SELECT * FROM users"
    print(row)  # => Output: (1, 'Alice')
    # => proves "*" returned EVERY column, not just a subset
