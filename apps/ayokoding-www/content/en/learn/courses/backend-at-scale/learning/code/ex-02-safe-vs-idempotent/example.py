# pyright: strict
"""Example 2: Safe vs Idempotent -- repeat GET, PUT, POST. (co-01)

RFC 9110 marks GET safe+idempotent and PUT idempotent, but POST NEITHER.
Calling the SAME request twice: GET and PUT reach the SAME end state, while
POST creates a SECOND resource. Source: RFC 9110 Sec 9.2.1-9.2.2 (STD 97).
"""

from dataclasses import dataclass  # => a small typed record for each call's footprint


@dataclass(frozen=True)  # => frozen: one row of the RFC 9110 method table, never mutated
class MethodFact:  # => co-01: the safe/idempotent classification for one method
    method: str  # => the HTTP method this row documents
    safe: bool  # => read-only -- no server state change (GET/HEAD/OPTIONS/TRACE)
    idempotent: bool  # => repeatable -- N calls == 1 call's end state (GET/PUT/DELETE/...)


RFC9110_METHODS: tuple[MethodFact, ...] = (  # => co-01: the authoritative table from RFC 9110
    MethodFact("GET", safe=True, idempotent=True),  # => read-only, repeatable
    MethodFact("PUT", safe=False, idempotent=True),  # => writes, but repeatable to the same end state
    MethodFact("POST", safe=False, idempotent=False),  # => writes AND each call creates anew
    MethodFact("DELETE", safe=False, idempotent=True),  # => removes, repeatable (second delete is a no-op)
)  # => end of the RFC 9110 method table

STORE: dict[int, str] = {}  # => the in-memory resource store, reset between demos
NEXT_ID = [1]  # => a mutable counter cell


def get(item_id: int) -> str:  # => GET: returns the value WITHOUT mutating STORE
    return STORE.get(item_id, "<missing>")  # => co-01: safe -- no side effect


def put(item_id: int, value: str) -> None:  # => PUT: SETS this exact key -- repeatable
    STORE[item_id] = value  # => co-01: idempotent -- two identical PUTs leave STORE identical


def post(value: str) -> int:  # => POST: mints a NEW id every call -- NOT repeatable
    new_id = NEXT_ID[0]  # => a fresh id each time
    STORE[new_id] = value  # => a brand-new entry
    NEXT_ID[0] += 1  # => advances the counter so the NEXT call differs
    return new_id


# GET twice: safe+idempotent -- STORE never changes.
STORE[1] = "v1"  # => seed one item so GET has something to read
get(1)
get(1)  # => two reads, zero writes -- co-01: safe
print(f"GET twice, store unchanged: {STORE}")  # => Output: {1: 'v1'}

# PUT twice: idempotent -- same key set to the same value twice == one end state.
put(1, "v2")
put(1, "v2")  # => co-01: two identical PUTs collapse to ONE final value
print(f"PUT twice, one final value: {STORE}")  # => Output: {1: 'v2'}

# POST twice: NOT idempotent -- two resources created.
STORE.clear()
NEXT_ID[0] = 1  # => reset for a clean POST demo
post("dup")
post("dup")  # => co-01: SAME body, TWO different ids
print(f"POST twice, two resources: {STORE}")  # => Output: {1: 'dup', 2: 'dup'}

# Mechanically confirm the table: POST is the only method here that is NOT idempotent.
non_idempotent = [m.method for m in RFC9110_METHODS if not m.idempotent]  # => co-01
print(f"methods that are NOT idempotent: {non_idempotent}")  # => Output: ['POST']
