"""Example 7: select() Lists Explicit Columns, in Order."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => dataclasses.replace() is the immutable "update" primitive
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass(frozen=True)  # => co-03: immutable, one method per fluent step
class Select:  # => the growing SELECT builder -- this example only exercises columns
    columns: tuple[str, ...] = ()  # => the SELECT list, empty means "not chosen yet"
    table: str | None = None  # => FROM target, filled in by .from_() (Example 8)

    def from_(self, table: str) -> "Select":  # => sets the FROM target, immutably
        return dataclasses.replace(self, table=table)  # => new instance, self untouched

    def compile(self) -> str:  # => co-04: assembles the SELECT clause from state
        col_list = ", ".join(self.columns) if self.columns else "*"  # => join or fall back
        return f"SELECT {col_list} FROM {self.table}"  # => the final assembled SQL string


def select(*columns: str) -> Select:  # => the public entry point: select("id", "name")
    return Select(columns=columns)  # => columns arrive as a tuple, in call order


query = select("id", "name").from_("users")  # => explicit two-column projection
sql = query.compile()  # => renders the accumulated state to SQL text
assert sql == "SELECT id, name FROM users"  # => "id" precedes "name" -- source order kept

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")  # => 3 cols
    conn.execute("INSERT INTO users(id, name, age) VALUES (1, 'Alice', 30)")  # => one seed row
    conn.commit()  # => makes the seed row visible to the SELECT below
    row = conn.execute(sql).fetchone()  # => runs the compiled two-column SELECT for real
    print(row)  # => Output: (1, 'Alice')
    # => proves the row has EXACTLY two fields -- age was never requested, never returned
