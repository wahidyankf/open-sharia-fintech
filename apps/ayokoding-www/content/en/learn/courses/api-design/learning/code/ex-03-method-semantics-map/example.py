# pyright: strict
"""Example 3: Mapping CRUD onto HTTP Methods. (co-06)

Each CRUD operation has one HTTP method it maps to most naturally under
RFC 9110's method semantics. This example builds that map explicitly, once,
so every later example (idempotency, status codes) can rely on the same
vocabulary instead of re-deriving it per endpoint.
"""

from dataclasses import dataclass  # => a small, typed record beats a bare tuple here


@dataclass(frozen=True)  # => frozen: this mapping is a fixed fact, never mutated at runtime
class MethodSemantics:  # => co-06: one row of the CRUD -> HTTP-method table
    # => frozen=True means attempting `row.http_method = "X"` later raises at runtime
    crud_action: str  # => the CRUD verb this row documents (Create/Read/Update/Delete)
    http_method: str  # => the HTTP method RFC 9110 assigns that intent
    intent: str  # => a one-line description of what the method actually DOES


CRUD_TO_HTTP: tuple[MethodSemantics, ...] = (  # => the fixed, ordered table itself
    MethodSemantics("Create", "POST", "create a new subordinate resource"),  # => co-06
    MethodSemantics("Read", "GET", "retrieve a representation, no side effects"),  # => co-06
    MethodSemantics("Update (replace)", "PUT", "replace the WHOLE resource"),  # => co-06
    MethodSemantics("Update (partial)", "PATCH", "apply a PARTIAL modification"),  # => co-06
    MethodSemantics("Delete", "DELETE", "remove the resource"),  # => co-06
)  # => a fixed, ordered mapping -- five rows, one per CRUD verb
# => CRUD_TO_HTTP has exactly 5 elements, one MethodSemantics per CRUD verb

for row in CRUD_TO_HTTP:  # => print every row of the mapping table
    print(f"{row.crud_action:<18} -> {row.http_method:<6} ({row.intent})")  # => Output: 5 aligned lines
    # => each line reads "<CRUD verb padded to 18> -> <HTTP method padded to 6> (<intent>)"
