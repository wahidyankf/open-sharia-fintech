# pyright: strict
"""Capstone: query_builder.py -- an immutable fluent query builder that compiles to
parameterized SQL, composed from co-01 (SQL as data), co-02 (parameterized SQL), co-03
(immutable fluent builder), co-05 (WHERE composition), co-07 (INSERT/UPDATE/DELETE
builders), and co-08 (compile() -> (sql, params)). This single module IS the capstone's
Step 1 deliverable: every later step (mapper.py, unit_of_work.py, lazy.py) issues its SQL
through this builder, never through a hand-written string.
"""

import dataclasses


@dataclasses.dataclass(frozen=True)  # => co-03: frozen -- every "mutation" returns a NEW instance
class Eq:  # => co-05: the one comparison this capstone's WHERE clauses need -- column = ?
    column: str  # => the column name, rendered verbatim (never a bound value)
    value: object  # => the bound value -- ALWAYS a parameter, never interpolated (co-02)


@dataclasses.dataclass(frozen=True)  # => co-03: a Select is itself immutable data, not a string
class Select:
    table: str  # => the FROM target
    _columns: tuple[str, ...] = ()  # => empty tuple means "SELECT *" (co-08's compile() decides)
    _wheres: tuple[Eq, ...] = ()  # => zero or more equality predicates, ANDed together

    def columns(self, *names: str) -> "Select":  # => co-03: returns a NEW Select, self is untouched
        return dataclasses.replace(self, _columns=self._columns + names)

    def where(self, column: str, value: object) -> "Select":  # => co-03 + co-05: branch immutably
        return dataclasses.replace(self, _wheres=self._wheres + (Eq(column, value),))

    def compile(self) -> tuple[str, list[object]]:  # => co-08: the ONE builder-to-driver boundary
        cols = ", ".join(self._columns) if self._columns else "*"  # => co-08: default SELECT *
        sql = f"SELECT {cols} FROM {self.table}"  # => the FROM clause, always present
        params: list[object] = []  # => co-02: every bound value collected here, in order
        if self._wheres:  # => co-05: WHERE is optional -- omitted entirely when there are none
            clauses = " AND ".join(f"{w.column} = ?" for w in self._wheres)  # => co-02: "?" placeholders only
            sql += f" WHERE {clauses}"  # => appended after FROM, never before
            params.extend(w.value for w in self._wheres)  # => co-02: values collected, never inlined
        return sql, params  # => co-08: ALWAYS a 2-tuple, (sql text, bound params list)


def select(table: str) -> Select:  # => a small factory -- reads better than Select(table) at call sites
    return Select(table)


@dataclasses.dataclass(frozen=True)  # => co-07: INSERT gets its own immutable builder shape
class Insert:
    table: str
    _values: tuple[tuple[str, object], ...] = ()  # => (column, value) pairs, in call order

    def values(self, **columns: object) -> "Insert":  # => co-03: returns a NEW Insert
        return dataclasses.replace(self, _values=self._values + tuple(columns.items()))

    def compile(self) -> tuple[str, list[object]]:  # => co-08: same compile() contract as Select
        cols = ", ".join(name for name, _ in self._values)  # => column list, in the order values() saw them
        placeholders = ", ".join("?" for _ in self._values)  # => co-02: one "?" per bound value, never a literal
        sql = f"INSERT INTO {self.table} ({cols}) VALUES ({placeholders})"
        params: list[object] = [value for _, value in self._values]  # => co-02: left-to-right, matching cols
        return sql, params


def insert(table: str) -> Insert:  # => factory, mirrors select()
    return Insert(table)


@dataclasses.dataclass(frozen=True)  # => co-07: UPDATE reuses Eq for its WHERE, exactly like Select
class Update:
    table: str
    _sets: tuple[tuple[str, object], ...] = ()  # => (column, new value) pairs -- co-17's dirty columns land here
    _wheres: tuple[Eq, ...] = ()

    def set(self, **columns: object) -> "Update":  # => co-03: returns a NEW Update
        return dataclasses.replace(self, _sets=self._sets + tuple(columns.items()))

    def where(self, column: str, value: object) -> "Update":  # => co-05: same WHERE machinery as Select
        return dataclasses.replace(self, _wheres=self._wheres + (Eq(column, value),))

    def compile(self) -> tuple[str, list[object]]:  # => co-08
        set_clause = ", ".join(f"{name} = ?" for name, _ in self._sets)  # => co-02: "?" per SET column
        sql = f"UPDATE {self.table} SET {set_clause}"
        params: list[object] = [value for _, value in self._sets]  # => SET params come first (co-08's order)
        if self._wheres:  # => co-05: WHERE is optional, but every UPDATE here always supplies one
            clauses = " AND ".join(f"{w.column} = ?" for w in self._wheres)
            sql += f" WHERE {clauses}"
            params.extend(w.value for w in self._wheres)  # => WHERE params come AFTER SET params
        return sql, params


def update(table: str) -> Update:  # => factory, mirrors select()/insert()
    return Update(table)


@dataclasses.dataclass(frozen=True)  # => co-07: DELETE is the smallest of the four builders
class Delete:
    table: str
    _wheres: tuple[Eq, ...] = ()

    def where(self, column: str, value: object) -> "Delete":  # => co-05
        return dataclasses.replace(self, _wheres=self._wheres + (Eq(column, value),))

    def compile(self) -> tuple[str, list[object]]:  # => co-08
        sql = f"DELETE FROM {self.table}"
        params: list[object] = []
        if self._wheres:  # => co-05: a DELETE with no WHERE would delete every row -- never used unguarded here
            clauses = " AND ".join(f"{w.column} = ?" for w in self._wheres)
            sql += f" WHERE {clauses}"
            params.extend(w.value for w in self._wheres)
        return sql, params


def delete(table: str) -> Delete:  # => factory, mirrors select()/insert()/update()
    return Delete(table)


if __name__ == "__main__":  # => guards against running the demo on `import query_builder`
    base = select("customer").columns("id", "name")  # => co-03: build once
    branch_a = base.where("id", 1)  # => co-03: branch A -- base is untouched by this call
    branch_b = base.where("id", 2)  # => co-03: branch B -- independent of branch A
    print(base.compile())  # => Output: ('SELECT id, name FROM customer', [])
    print(branch_a.compile())  # => Output: ('SELECT id, name FROM customer WHERE id = ?', [1])
    print(branch_b.compile())  # => Output: ('SELECT id, name FROM customer WHERE id = ?', [2])
    assert base.compile() == ("SELECT id, name FROM customer", [])  # => co-03: base never mutated
    hostile = "1; DROP TABLE customer;--"  # => a deliberately hostile string, never interpolated (co-02)
    sql, params = select("customer").where("name", hostile).compile()
    print(sql, params)  # => Output: SELECT * FROM customer WHERE name = ? ['1; DROP TABLE customer;--']
    assert "DROP TABLE" not in sql  # => co-02: the hostile text lives ONLY in params, never in the SQL text
