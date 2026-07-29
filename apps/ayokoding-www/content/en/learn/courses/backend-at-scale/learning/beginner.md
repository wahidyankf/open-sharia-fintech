---
title: "Beginner Examples"
date: 2026-07-29T00:00:00+07:00
draft: false
weight: 10
---

Examples 1-28 cover the foundations every later example builds on: RFC 9110's method safety/idempotency, the status codes that distinguish one outcome from another (201/204/400/401/403/409/422), URI-path and header versioning, offset and cursor pagination (and why cursor is stable under concurrent inserts), Idempotency-Key record/replay/reject-on-mismatch, the repository and unit-of-work patterns over an in-memory store, ACID transaction atomicity, JWT encode/verify and expiry, RBAC vs ABAC gates, and structured JSON logging with a threaded correlation id. Every example is a complete, self-contained, originally-authored Python 3 script using only the standard library -- no framework, driver, or network connection is required. Run each with `python3 example.py`; every printed line below was captured from an actual run of the file shown, not hand-traced.

---

### Example 1: REST CRUD Endpoints -- One Resource, Four Verbs

_ex-01 &middot; exercises co-01_

Each CRUD operation maps to one HTTP verb over the same `/tasks` resource. This example routes every verb to its own handler and verifies each produces the effect its RFC 9110 semantics promise.

**`learning/code/ex-01-rest-crud-endpoints/example.py`**

```python
# pyright: strict
"""Example 1: REST CRUD Endpoints -- one resource, four verbs. (co-01)

GET/POST/PUT/DELETE each take their OWN path to the SAME /tasks resource.
This example routes every verb to its own handler over one in-memory store
and verifies each verb produces the effect its RFC 9110 semantics promise.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-01: the shape every handler below returns -- status + body
class Response:
    status: int  # => the HTTP status code this verb produced
    body: dict[str, object] = field(default_factory=dict[str, object])  # => resource or error payload


STORE: dict[int, str] = {1: "Write tests", 2: "Ship feature"}  # => co-01: the in-memory /tasks store
NEXT_ID = [3]  # => a mutable counter cell -- the next id a POST will mint


def handle_get() -> Response:  # => GET /tasks -- READ, safe + idempotent (co-01)
    return Response(status=200, body={"tasks": {i: t for i, t in STORE.items()}})  # => returns the whole collection


def handle_post(title: str) -> Response:  # => POST /tasks -- CREATE, neither safe nor idempotent (co-01)
    new_id = NEXT_ID[0]  # => mints a brand-new id on every call
    STORE[new_id] = title  # => adds a NEW member to the collection
    NEXT_ID[0] += 1  # => advances the counter for the next create
    return Response(status=201, body={"id": new_id, "title": title})  # => 201 Created


def handle_put(task_id: int, title: str) -> Response:  # => PUT /tasks/{id} -- REPLACE, idempotent (co-01)
    if task_id not in STORE:  # => no such resource -> 404, PUT to a missing id cannot invent it here
        return Response(status=404, body={"error": "not found"})  # => 404
    STORE[task_id] = title  # => OVERWRITES the resource with the given representation
    return Response(status=200, body={"id": task_id, "title": title})  # => 200, replaced


def handle_delete(task_id: int) -> Response:  # => DELETE /tasks/{id} -- REMOVE, idempotent (co-01)
    if task_id not in STORE:  # => already gone -> 404
        return Response(status=404, body={"error": "not found"})  # => 404
    del STORE[task_id]  # => removes the member from the collection
    return Response(status=204, body={})  # => 204 No Content


get = handle_get()  # => GET: reads the collection, no side effect
print(f"GET    -> status={get.status}, tasks={get.body['tasks']}")  # => Output: 200, both seeded tasks

created = handle_post("Review PR")  # => POST: creates a new task
print(f"POST   -> status={created.status}, created={created.body}")  # => Output: 201, id=3

replaced = handle_put(1, "Write MORE tests")  # => PUT: replaces task 1's title
print(f"PUT    -> status={replaced.status}, replaced={replaced.body}")  # => Output: 200, new title

deleted = handle_delete(2)  # => DELETE: removes task 2
print(f"DELETE -> status={deleted.status}, body={deleted.body}")  # => Output: 204, empty body

print(f"final store: {STORE}")  # => Output: task 1 replaced, task 2 gone, task 3 added
```

**Run**: `python3 example.py`

**Output**:

```text
GET    -> status=200, tasks={1: 'Write tests', 2: 'Ship feature'}
POST   -> status=201, created={'id': 3, 'title': 'Review PR'}
PUT    -> status=200, replaced={'id': 1, 'title': 'Write MORE tests'}
DELETE -> status=204, body={}
final store: {1: 'Write MORE tests', 3: 'Review PR'}
```

**Key takeaway**: GET reads, POST creates, PUT replaces, DELETE removes -- the verb carries the action, the path names the thing.

**Why it matters**: Every status-code, idempotency, and versioning example in this course assumes this CRUD-to-verb mapping; getting it right once means every later example can simply name a verb.

---

### Example 2: Safe vs Idempotent -- Repeat GET, PUT, POST

_ex-02 &middot; exercises co-01_

RFC 9110 marks GET safe+idempotent and PUT idempotent, but POST neither. Repeating the same request twice leaves GET/PUT in the same end state, while POST creates a second resource.

**`learning/code/ex-02-safe-vs-idempotent/example.py`**

```python
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
get(1); get(1)  # => two reads, zero writes -- co-01: safe
print(f"GET twice, store unchanged: {STORE}")  # => Output: {1: 'v1'}

# PUT twice: idempotent -- same key set to the same value twice == one end state.
put(1, "v2"); put(1, "v2")  # => co-01: two identical PUTs collapse to ONE final value
print(f"PUT twice, one final value: {STORE}")  # => Output: {1: 'v2'}

# POST twice: NOT idempotent -- two resources created.
STORE.clear(); NEXT_ID[0] = 1  # => reset for a clean POST demo
post("dup"); post("dup")  # => co-01: SAME body, TWO different ids
print(f"POST twice, two resources: {STORE}")  # => Output: {1: 'dup', 2: 'dup'}

# Mechanically confirm the table: POST is the only method here that is NOT idempotent.
non_idempotent = [m.method for m in RFC9110_METHODS if not m.idempotent]  # => co-01
print(f"methods that are NOT idempotent: {non_idempotent}")  # => Output: ['POST']
```

**Run**: `python3 example.py`

**Output**:

```text
GET twice, store unchanged: {1: 'v1'}
PUT twice, one final value: {1: 'v2'}
POST twice, two resources: {1: 'dup', 2: 'dup'}
methods that are NOT idempotent: ['POST']
```

**Key takeaway**: Idempotency is about the RESULT of repeating a request, not whether the method has side effects -- both PUT and POST write data, but only PUT's repeat leaves the store unchanged.

**Why it matters**: A client that auto-retries on a flaky network needs to know whether retrying is safe -- retrying PUT always is, blindly retrying POST can duplicate resources, which is exactly the gap the Idempotency-Key (co-06) closes.

---

### Example 3: 201 Created + Location

_ex-03 &middot; exercises co-02_

A successful POST that creates a resource returns 201 Created AND a Location header pointing at the new resource -- the status alone never says WHERE the new thing lives.

**`learning/code/ex-03-status-201-created/example.py`**

```python
# pyright: strict
"""Example 3: 201 Created + Location. (co-02)

A successful POST that creates a resource returns 201 Created AND a Location
header pointing at the new resource -- the status alone never says WHERE the
new thing lives; the header does. Source: RFC 9110 Sec 15.3.2.
"""

from dataclasses import dataclass, field  # => field: gives the headers dict its own factory


@dataclass  # => co-02: the two facts a caller needs -- status, and where the resource landed
class Response:
    status: int  # => the HTTP status code
    headers: dict[str, str] = field(default_factory=dict[str, str])  # => response headers (Location lives here)
    body: dict[str, object] = field(default_factory=dict[str, object])  # => the created resource representation


STORE: dict[int, dict[str, object]] = {}  # => in-memory resource store, keyed by id
NEXT_ID = [1]  # => a mutable counter cell -- the next id a create will mint


def create_task(title: str) -> Response:  # => POST /tasks -- creates a new subordinate resource
    new_id = NEXT_ID[0]  # => mints a fresh id for this new resource
    resource: dict[str, object] = {"id": new_id, "title": title}  # => the created representation
    STORE[new_id] = resource  # => persists it so a follow-up GET could find it
    NEXT_ID[0] += 1  # => advances the counter for the next create
    location = f"/tasks/{new_id}"  # => co-02: the URI of the JUST-CREATED resource
    return Response(status=201, headers={"Location": location}, body=resource)  # => 201 + Location, co-02's pair


response = create_task("Deploy to staging")  # => run the handler once
print(f"status={response.status}")  # => Output: 201
print(f"Location={response.headers['Location']}")  # => Output: /tasks/1
assert response.status == 201  # => co-02: confirms the status half of the contract
assert response.headers["Location"] == "/tasks/1"  # => confirms the Location half
print(f"created: {response.body}")  # => Output: the created representation, echoed back
```

**Run**: `python3 example.py`

**Output**:

```text
status=201
Location=/tasks/1
created: {'id': 1, 'title': 'Deploy to staging'}
```

**Key takeaway**: 201 alone tells a client 'something new exists' but not what to do next -- the Location header turns that into an actionable follow-up GET.

**Why it matters**: A client that ignores Location and constructs its own URL is fragile the moment the server-assigned id diverges from anything the client sent.

---

### Example 4: 204 No Content for DELETE

_ex-04 &middot; exercises co-02_

A successful DELETE has nothing left to represent, so RFC 9110 gives it 204 No Content: success, but an intentionally EMPTY body.

**`learning/code/ex-04-status-204-delete/example.py`**

```python
# pyright: strict
"""Example 4: 204 No Content for DELETE. (co-02)

A successful DELETE has nothing left to represent -- the resource is gone --
so RFC 9110 gives it 204 No Content: success, but an intentionally EMPTY
body, distinct from 200 OK's "success, and here is a representation."
"""

from dataclasses import dataclass  # => a small typed response record for this example


@dataclass  # => co-02: status plus a body kept as a plain str for a trivial emptiness check
class Response:
    status: int  # => the HTTP status code
    body: str  # => kept as a plain str so an EMPTY body is trivially checkable ("" == empty)


STORE: dict[int, str] = {1: "Draft task", 2: "Another task"}  # => two seeded resources to delete from


def delete_task(task_id: int) -> Response:  # => DELETE /tasks/{id}
    if task_id not in STORE:  # => no such resource -- nothing to delete
        return Response(status=404, body="not found")  # => 404, the resource never existed
    del STORE[task_id]  # => co-02: the resource is now genuinely gone from the store
    return Response(status=204, body="")  # => co-02: 204 -- success, deliberately empty body


response = delete_task(1)  # => delete the one seeded task
print(f"status={response.status}, body={response.body!r}")  # => Output: status=204, body=''
assert response.status == 204  # => co-02: confirms the "no content" status
assert response.body == ""  # => confirms the body is genuinely empty, not e.g. "null"
assert 1 not in STORE  # => confirms the underlying resource really was removed
print(f"remaining in store: {STORE}")  # => Output: only task 2 remains
```

**Run**: `python3 example.py`

**Output**:

```text
status=204, body=''
remaining in store: {2: 'Another task'}
```

**Key takeaway**: 204's empty body is a deliberate design choice -- a client should never try to json.loads() a 204 body.

**Why it matters**: Returning 200 with a null body for a DELETE forces every client to special-case parsing an 'empty-ish' body; 204 removes that ambiguity at the protocol level.

---

### Example 5: 400 Bad Request -- a Malformed Payload

_ex-05 &middot; exercises co-02_

A syntactically malformed request body (wrong type, missing required field, empty) is rejected with 400 Bad Request -- the server never reaches business logic.

**`learning/code/ex-05-status-400-validation/example.py`**

```python
# pyright: strict
"""Example 5: 400 Bad Request -- a malformed payload. (co-02)

A syntactically malformed request body (wrong type, missing required field)
is rejected with 400 Bad Request -- the server never reaches business logic
because the payload could not be parsed into the expected shape.
"""

from dataclasses import dataclass  # => a small typed response record for this example


@dataclass  # => co-02: status plus a small error body
class Response:
    status: int  # => the HTTP status code
    body: dict[str, str]  # => either an error message or the accepted payload


def parse_task_payload(raw: dict[str, object]) -> tuple[Response, str | None]:  # => returns (response, parsed title)
    # => co-02: validate BEFORE touching the store -- a malformed body is a 400, not a business error
    if "title" not in raw:  # => the required field is missing entirely
        return Response(400, {"error": "missing required field: title"}), None  # => 400, malformed
    title_value = raw["title"]  # => the value present at the title key
    if not isinstance(title_value, str):  # => the title is present but the WRONG TYPE (e.g. an int)
        return Response(400, {"error": "title must be a string"}), None  # => 400, malformed
    if title_value == "":  # => present and a string, but empty -- still malformed for this endpoint
        return Response(400, {"error": "title must not be empty"}), None  # => 400, malformed
    return Response(202, {"accepted": title_value}), title_value  # => accepted shape (202 just signals "ok" here)


missing = parse_task_payload({})  # => no title key at all
print(f"missing title:    status={missing[0].status}, body={missing[0].body}")  # => Output: 400

wrong_type = parse_task_payload({"title": 42})  # => title present but not a string
print(f"wrong type:       status={wrong_type[0].status}, body={wrong_type[0].body}")  # => Output: 400

empty = parse_task_payload({"title": ""})  # => title present, a string, but empty
print(f"empty title:      status={empty[0].status}, body={empty[0].body}")  # => Output: 400

ok = parse_task_payload({"title": "Valid task"})  # => a well-formed payload
print(f"well-formed:      status={ok[0].status}, body={ok[0].body}")  # => Output: 202, accepted

assert missing[0].status == 400 and wrong_type[0].status == 400 and empty[0].status == 400  # => co-02: all three are 400
```

**Run**: `python3 example.py`

**Output**:

```text
missing title:    status=400, body={'error': 'missing required field: title'}
wrong type:       status=400, body={'error': 'title must be a string'}
empty title:      status=400, body={'error': 'title must not be empty'}
well-formed:      status=202, body={'accepted': 'Valid task'}
```

**Key takeaway**: 400 is about the payload's SHAPE being unparseable, distinct from 422's 'parses but semantically invalid'.

**Why it matters**: Collapsing every rejection into 400 forces a client to string-match error messages; 400 vs 422 vs 409 let a client branch its remediation without parsing prose.

---

### Example 6: 401 Unauthorized vs 403 Forbidden

_ex-06 &middot; exercises co-02_

401 means authentication required and has failed or not been provided; 403 means the server refuses to authorize a VALID identity that lacks permission. The two are distinct.

**`learning/code/ex-06-status-401-vs-403/example.py`**

```python
# pyright: strict
"""Example 6: 401 Unauthorized vs 403 Forbidden. (co-02)

401 = authentication required and has failed or not been provided; 403 = the
server refuses to authorize a VALID identity that lacks permission. The two
are distinct: 401 is "who are you?", 403 is "I know who you are, but no."
Source: RFC 9110 Sec 15.5.1 (401) and Sec 15.5.4 (403).
"""

from dataclasses import dataclass  # => a small typed response record for this example


@dataclass  # => co-02: status plus an error message
class Response:
    status: int  # => the HTTP status code
    body: dict[str, str]  # => a short error explanation


# A toy token store: token -> (user, role). "admin" can delete; "viewer" cannot.
TOKENS: dict[str, tuple[str, str]] = {"tok-admin": ("ada", "admin"), "tok-viewer": ("grace", "viewer")}
REQUIRED_ROLE = "admin"  # => the role this protected operation demands


def delete_task(token: str | None, task_id: int) -> Response:  # => DELETE /tasks/{id}, auth-gated
    if token is None or token not in TOKENS:  # => co-02: no identity provided OR identity not recognized -> 401
        return Response(401, {"error": "authentication required"})  # => 401: "who are you?"
    _user, role = TOKENS[token]  # => identity is valid -- now check authorization
    if role != REQUIRED_ROLE:  # => co-02: valid identity, but lacks the required role -> 403
        return Response(403, {"error": "insufficient role"})  # => 403: "I know you, but no."
    return Response(204, {"deleted": str(task_id)})  # => authenticated AND authorized -> 204


no_token = delete_task(token=None, task_id=1)  # => no Authorization header at all
print(f"no token:     status={no_token.status}, body={no_token.body}")  # => Output: 401

bad_token = delete_task(token="tok-bogus", task_id=1)  # => a token the server does not recognize
print(f"bad token:    status={bad_token.status}, body={bad_token.body}")  # => Output: 401

wrong_role = delete_task(token="tok-viewer", task_id=1)  # => valid identity, but role "viewer" cannot delete
print(f"wrong role:   status={wrong_role.status}, body={wrong_role.body}")  # => Output: 403

ok = delete_task(token="tok-admin", task_id=1)  # => valid identity, correct role
print(f"admin:        status={ok.status}, body={ok.body}")  # => Output: 204

assert no_token.status == 401 and bad_token.status == 401  # => co-02: auth-missing is 401
assert wrong_role.status == 403  # => co-02: valid-auth-but-forbidden is 403
assert ok.status == 204  # => authorized
```

**Run**: `python3 example.py`

**Output**:

```text
no token:     status=401, body={'error': 'authentication required'}
bad token:    status=401, body={'error': 'authentication required'}
wrong role:   status=403, body={'error': 'insufficient role'}
admin:        status=204, body={'deleted': '1'}
```

**Key takeaway**: 401 is 'who are you?' and 403 is 'I know who you are, but no' -- conflating them misleads every client's retry and re-auth logic.

**Why it matters**: A valid token that lacks a role must return 403, not 401 -- otherwise a client wrongly concludes its credentials are bad and re-prompts the user forever.

---

### Example 7: 409 Conflict -- a Duplicate Create

_ex-07 &middot; exercises co-02_

409 Conflict means the request collides with the resource's CURRENT state -- here, a username that already exists.

**`learning/code/ex-07-status-409-conflict/example.py`**

```python
# pyright: strict
"""Example 7: 409 Conflict -- a duplicate create. (co-02)

409 Conflict means the request collides with the resource's CURRENT state --
here, creating a username that already exists. The request itself is well-
formed, but applying it right now would duplicate a unique value. Source:
RFC 9110 Sec 15.5.10.
"""

from dataclasses import dataclass  # => a small typed response record for this example


@dataclass  # => co-02: status plus an error or success body
class Response:
    status: int  # => the HTTP status code
    body: dict[str, str]  # => either an error message or the created resource


USERNAMES: set[str] = {"ada"}  # => the "current state" a 409 uniqueness check compares against


def create_user(username: str) -> Response:  # => POST /users -- can succeed or collide
    if username in USERNAMES:  # => co-02: collides with EXISTING state -- a conflict, not a syntax error
        return Response(409, {"error": f"username {username!r} already taken"})  # => 409, state clash
    USERNAMES.add(username)  # => no collision -- the write actually happens
    return Response(201, {"username": username})  # => success, resource created


conflict = create_user("ada")  # => "ada" already exists -> conflict
print(f"duplicate: status={conflict.status}, body={conflict.body}")  # => Output: 409

created = create_user("grace")  # => a brand-new username -> succeeds
print(f"new user:  status={created.status}, body={created.body}")  # => Output: 201

second_conflict = create_user("grace")  # => "grace" now also exists -> conflict
print(f"duplicate: status={second_conflict.status}, body={second_conflict.body}")  # => Output: 409

assert conflict.status == 409 and second_conflict.status == 409  # => co-02: both duplicates are 409
assert created.status == 201  # => the genuinely new one succeeded
```

**Run**: `python3 example.py`

**Output**:

```text
duplicate: status=409, body={'error': "username 'ada' already taken"}
new user:  status=201, body={'username': 'grace'}
duplicate: status=409, body={'error': "username 'grace' already taken"}
```

**Key takeaway**: 409 is a collision with EXISTING state; the request itself is well-formed, but applying it now would duplicate a unique value.

**Why it matters**: A client seeing 409 knows to retry with a different value, whereas 422 means 'fix this field' -- genuinely different remediation paths.

---

### Example 8: 422 Unprocessable Content

_ex-08 &middot; exercises co-02_

RFC 9110 Sec 15.5.21 defines 422 'Unprocessable Content' (renamed from RFC 4918's 'Unprocessable Entity'). The JSON parses fine, but a field fails a business rule.

**`learning/code/ex-08-status-422-unprocessable/example.py`**

```python
# pyright: strict
"""Example 8: 422 Unprocessable Content -- well-formed but semantically invalid. (co-02)

RFC 9110 Sec 15.5.21 defines 422 "Unprocessable Content" (renamed from
RFC 4918's WebDAV-era "Unprocessable Entity"). The JSON parses fine, but a
field fails a BUSINESS rule -- here, a negative age. RFC 9110 does NOT
obsolete RFC 4918; they coexist. Teach "Unprocessable Content".
"""

from dataclasses import dataclass  # => a small typed response record for this example


@dataclass  # => co-02: status plus an error or success body
class Response:
    status: int  # => the HTTP status code
    body: dict[str, object]  # => either a field error or the created resource


def create_user(username: str, age: int) -> Response:  # => POST /users -- syntactically valid, semantically checked
    if age < 0:  # => co-02: a valid integer, but a nonsensical VALUE -- semantic, not syntactic
        return Response(422, {"error": "age must be non-negative", "field": "age"})  # => 422, semantic failure
    return Response(201, {"username": username, "age": age})  # => success, resource created


negative_age = create_user("grace", -5)  # => a well-formed body, but a semantically invalid age
print(f"negative age: status={negative_age.status}, body={negative_age.body}")  # => Output: 422

valid = create_user("grace", 37)  # => a fully valid input
print(f"valid:        status={valid.status}, body={valid.body}")  # => Output: 201

# Contrast with a 400 (Example 5): here the JSON parsed fine -- the failure is the VALUE's meaning.
assert negative_age.status == 422  # => co-02: semantic failure is 422, not 400
assert valid.status == 201  # => a valid value succeeds
```

**Run**: `python3 example.py`

**Output**:

```text
negative age: status=422, body={'error': 'age must be non-negative', 'field': 'age'}
valid:        status=201, body={'username': 'grace', 'age': 37}
```

**Key takeaway**: 422 is a well-formed body with a semantically invalid VALUE -- distinct from 400's malformed shape.

**Why it matters**: Teaching 'Unprocessable Content' (not the older 'Entity') keeps the course aligned with the current RFC 9110 wording.

---

### Example 9: Versioning via the URI Path

_ex-09 &middot; exercises co-03_

Routing the version into the URI path (/v1/tasks vs /v2/tasks) is the strategy Google's AIP-185 names. The version lives in the URL, so a CDN naturally treats each version as distinct.

**`learning/code/ex-09-version-uri-path/example.py`**

```python
# pyright: strict
"""Example 9: Versioning via the URI Path -- /v1/ vs /v2/. (co-03)

Routing the version into the URI path (/v1/tasks vs /v2/tasks) is the
strategy Google's AIP-185 names ("major version in the URI, e.g. v1 not
v1.0"). The version lives in the URL, so an HTTP cache or CDN naturally
treats each version as a distinct entry with no special config.
"""

from collections.abc import Callable  # => Callable: the type of the version-specific handlers
from dataclasses import dataclass  # => a small typed response record for each version


@dataclass  # => co-03: one version's own response shape -- v1 and v2 differ deliberately
class Response:
    status: int  # => the HTTP status code
    body: dict[str, object]  # => the version-specific representation


def tasks_v1() -> Response:  # => /v1/tasks -- the original representation (title only)
    return Response(200, {"version": 1, "tasks": [{"id": 1, "title": "Legacy task"}]})  # => co-03: v1 shape


def tasks_v2() -> Response:  # => /v2/tasks -- the evolved representation (title + status added)
    return Response(200, {"version": 2, "tasks": [{"id": 1, "title": "Legacy task", "status": "open"}]})  # => co-03: v2 adds a field


ROUTES: dict[str, Callable[[], Response]] = {"/v1/tasks": tasks_v1, "/v2/tasks": tasks_v2}  # => co-03: version baked INTO the path


def route(path: str) -> Response:  # => a tiny path-based router
    handler = ROUTES.get(path)  # => looks up the handler for this exact versioned path
    if handler is None:  # => unknown path or unknown version -> 404
        return Response(404, {"error": f"no route for {path}"})  # => 404
    return handler()  # => invokes the version-specific handler


v1 = route("/v1/tasks")  # => resolves to the v1 handler
print(f"/v1/tasks -> status={v1.status}, body={v1.body}")  # => Output: version 1, title only

v2 = route("/v2/tasks")  # => resolves to the v2 handler
print(f"/v2/tasks -> status={v2.status}, body={v2.body}")  # => Output: version 2, title + status

missing = route("/v3/tasks")  # => a version that was never published -> 404
print(f"/v3/tasks -> status={missing.status}, body={missing.body}")  # => Output: 404

assert v1.body["version"] == 1 and v2.body["version"] == 2  # => co-03: each version resolves to its own handler
```

**Run**: `python3 example.py`

**Output**:

```text
/v1/tasks -> status=200, body={'version': 1, 'tasks': [{'id': 1, 'title': 'Legacy task'}]}
/v2/tasks -> status=200, body={'version': 2, 'tasks': [{'id': 1, 'title': 'Legacy task', 'status': 'open'}]}
/v3/tasks -> status=404, body={'error': 'no route for /v3/tasks'}
```

**Key takeaway**: URI-path versioning bakes the version into the cache key for free, at the cost of URL churn across major versions.

**Why it matters**: The versioning strategy affects HTTP-cache compatibility and discoverability -- there is no single right answer, only named forces.

---

### Example 10: Versioning via a Request Header

_ex-10 &middot; exercises co-03_

Selecting the version from a request header (Stripe's Stripe-Version style) keeps the URL identical across versions but asks the client to opt into one.

**`learning/code/ex-10-version-header/example.py`**

```python
# pyright: strict
"""Example 10: Versioning via a Request Header. (co-03)

Selecting the version from a request header (e.g. Stripe's `Stripe-Version`)
keeps the URL identical across versions but asks the client to opt into one.
The trade-off: a cache keyed only on the URL now needs extra configuration to
avoid conflating two versions under the same cached URL.
"""

from dataclasses import dataclass  # => a small typed response record for each version


@dataclass  # => co-03: one version's own response shape
class Response:
    status: int  # => the HTTP status code
    body: dict[str, object]  # => the version-specific representation


@dataclass  # => co-03: a request carries a path AND a version-selecting header
class Request:
    path: str  # => the (version-free) resource path
    headers: dict[str, str]  # => the version is selected HERE, not in the URL


def tasks_v1() -> Response:  # => the original representation
    return Response(200, {"version": 1, "tasks": [{"id": 1, "title": "Legacy task"}]})  # => v1 shape


def tasks_v2() -> Response:  # => the evolved representation (a field added)
    return Response(200, {"version": 2, "tasks": [{"id": 1, "title": "Legacy task", "status": "open"}]})  # => v2 adds status


VERSION_HEADER = "X-API-Version"  # => the header name this API selects the version with


def route(request: Request) -> Response:  # => a header-based router -- the URL is the SAME for both versions
    version = request.headers.get(VERSION_HEADER, "1")  # => defaults to v1 when the header is absent
    if version == "1":  # => co-03: the client opted into v1 (or sent nothing)
        return tasks_v1()  # => v1 handler
    if version == "2":  # => co-03: the client opted into v2
        return tasks_v2()  # => v2 handler
    return Response(404, {"error": f"unknown version {version}"})  # => an unrecognized version


default_req = Request(path="/tasks", headers={})  # => no version header -> defaults to v1
print(f"no header (default v1): version={route(default_req).body['version']}")  # => Output: 1

v1_req = Request(path="/tasks", headers={VERSION_HEADER: "1"})  # => explicitly v1
print(f"header=1:               version={route(v1_req).body['version']}")  # => Output: 1

v2_req = Request(path="/tasks", headers={VERSION_HEADER: "2"})  # => explicitly v2 -- SAME path as v1
print(f"header=2:               version={route(v2_req).body['version']}")  # => Output: 2

# Same URL, two versions: a cache keyed only on /tasks would conflate them -- the header-versioning trade-off.
assert route(v1_req).body["version"] == 1 and route(v2_req).body["version"] == 2  # => co-03
print(f"same path '/tasks' served versions 1 and 2 by header")  # => Output: header routing confirmed
```

**Run**: `python3 example.py`

**Output**:

```text
no header (default v1): version=1
header=1:               version=1
header=2:               version=2
same path '/tasks' served versions 1 and 2 by header
```

**Key takeaway**: Header versioning keeps URLs clean, but a cache keyed only on the URL now needs extra configuration to avoid conflating two versions.

**Why it matters**: The trade-off vs URI-path is concrete: header versioning trades URL stability for cache-key complexity.

---

### Example 11: Offset/Limit Pagination

_ex-11 &middot; exercises co-04_

?offset=20&limit=10 asks the server to SKIP 20 rows and return the NEXT 10. This example builds the slicing and verifies the correct window returns.

**`learning/code/ex-11-offset-limit-page/example.py`**

```python
# pyright: strict
"""Example 11: Offset/Limit Pagination -- the correct slice. (co-04)

?offset=20&limit=10 asks the server to SKIP 20 rows and return the NEXT 10.
This example builds the slicing and verifies the correct window (rows 21..30)
comes back. The fetch-and-discard COST of that skip is the subject of Example 12.
"""

from dataclasses import dataclass  # => a small typed response record for a page


@dataclass  # => co-04: a page of items plus a pointer to keep paging
class Page:
    data: list[int]  # => the items on THIS page (their ids)
    offset: int  # => the offset this page started at
    limit: int  # => the limit (count) requested
    total: int  # => the full collection size, so the caller knows if more pages exist


ROWS: list[int] = list(range(1, 101))  # => 100 rows, ids 1..100 -- the collection being paged


def page_offset_limit(offset: int, limit: int) -> Page:  # => co-04: GET /items?offset=20&limit=10
    start = offset  # => the number of rows to SKIP
    window = ROWS[start : start + limit]  # => co-04: the next `limit` rows after skipping `offset`
    return Page(data=window, offset=offset, limit=limit, total=len(ROWS))  # => the page envelope


page = page_offset_limit(offset=20, limit=10)  # => skip 20, take 10 -- rows 21..30
print(f"offset=20, limit=10 -> first={page.data[0]}, last={page.data[-1]}, count={len(page.data)}")  # => Output: 21, 30, 10

first_page = page_offset_limit(offset=0, limit=10)  # => the very first page
print(f"offset=0, limit=10  -> first={first_page.data[0]}, last={first_page.data[-1]}")  # => Output: 1, 10

assert page.data == list(range(21, 31))  # => co-04: exactly rows 21 through 30
assert len(page.data) == page.limit  # => the page respects the requested count
```

**Run**: `python3 example.py`

**Output**:

```text
offset=20, limit=10 -> first=21, last=30, count=10
offset=0, limit=10  -> first=1, last=10
```

**Key takeaway**: Offset/limit means 'skip N, take M' -- simple, but the skip pays a fetch-and-discard cost (Example 12).

**Why it matters**: Understanding the offset cost is the specific motivation for cursor pagination (co-05) once a dataset grows or churns.

---

### Example 12: Offset Pagination's Fetch-and-Discard Cost

_ex-12 &middot; exercises co-04_

OFFSET makes the database 'fetch and discard' every preceding row: to serve offset=5000 it walks past 5000 rows before returning 10. The instrumented counter shows the cost grows linearly.

**`learning/code/ex-12-offset-cost-demo/example.py`**

```python
# pyright: strict
"""Example 12: Offset Pagination's Cost -- fetch-and-discard. (co-04)

OFFSET makes the database "fetch and discard" every preceding row: to serve
offset=1000 it must walk past 1000 rows before returning the requested 10.
This example instruments a simulated query with a row-touch counter and shows
the touch count grows linearly with the offset. Source: "Use The Index, Luke
-- No Offset" (Markus Winand).
"""

ROWS_TOUCHED = [0]  # => a mutable counter cell -- how many rows the "query" scanned


def fetch_with_offset(offset: int, limit: int, table: list[int]) -> list[int]:
    ROWS_TOUCHED[0] = 0  # => reset the counter for this query
    page: list[int] = []  # => the rows actually returned
    for index, row in enumerate(table):  # => simulate the DB scanning the table in order
        ROWS_TOUCHED[0] += 1  # => EVERY row the scan passes is "touched", even skipped ones
        if index < offset:  # => co-04: rows before the offset are FETCHED then DISCARDED
            continue  # => touched but not returned -- this is the cost
        page.append(row)  # => a row that is BOTH touched AND returned
        if len(page) >= limit:  # => the page is full
            break  # => stop scanning immediately -- no extra row touched
    return page


TABLE = list(range(1, 10001))  # => 10000 rows -- a large enough table to make the cost visible

shallow = fetch_with_offset(offset=0, limit=10, table=TABLE)  # => page 1: touches only 10 rows
print(f"offset=0, limit=10    -> returned {len(shallow)} rows, touched {ROWS_TOUCHED[0]} rows")  # => Output: 10 touched

deep = fetch_with_offset(offset=1000, limit=10, table=TABLE)  # => page ~101: touches 1010 rows
print(f"offset=1000, limit=10 -> returned {len(deep)} rows, touched {ROWS_TOUCHED[0]} rows")  # => Output: 1010 touched

deeper = fetch_with_offset(offset=5000, limit=10, table=TABLE)  # => a deep page: touches 5010 rows
print(f"offset=5000, limit=10 -> returned {len(deeper)} rows, touched {ROWS_TOUCHED[0]} rows")  # => Output: 5010 touched

# The returned COUNT is always 10, but the touched count grows linearly with offset -- the fetch-and-discard cost.
assert len(shallow) == len(deep) == len(deeper) == 10  # => same page size
assert ROWS_TOUCHED[0] == 5010  # => the deep page paid for 5010 touches to return 10 rows
```

**Run**: `python3 example.py`

**Output**:

```text
offset=0, limit=10    -> returned 10 rows, touched 10 rows
offset=1000, limit=10 -> returned 10 rows, touched 1010 rows
offset=5000, limit=10 -> returned 10 rows, touched 5010 rows
```

**Key takeaway**: The returned count is always 10, but the touched count grows linearly with the offset -- that is the fetch-and-discard cost.

**Why it matters**: Source: 'Use The Index, Luke -- No Offset' (Markus Winand). This cost is exactly what cursor paging avoids.

---

### Example 13: Cursor Pagination -- Resume After a Key

_ex-13 &middot; exercises co-05_

A cursor encodes a position IN THE DATA (the last-seen id) and the next page resumes with WHERE id > cursor -- Stripe calls this starting_after.

**`learning/code/ex-13-cursor-page/example.py`**

```python
# pyright: strict
"""Example 13: Cursor Pagination -- resume after a key. (co-05)

A cursor encodes a position IN THE DATA (the last-seen item's sort key) and
the next page resumes with `WHERE id > cursor`. This avoids the fetch-and-
discard cost and is stable under concurrent inserts. Stripe's API calls this
`starting_after`. Source: Stripe pagination docs; "Use The Index, Luke".
"""

from dataclasses import dataclass  # => a small typed response record for a page


@dataclass  # => co-05: a page of items plus the cursor to fetch the next page
class Page:
    data: list[int]  # => the ids on THIS page
    next_cursor: int | None  # => the last id on this page, or None when the end is reached


ROWS: list[int] = list(range(1, 101))  # => 100 rows, ids 1..100, sorted ascending (the indexed key)


def page_starting_after(starting_after: int | None, limit: int) -> Page:  # => co-05: GET /items?starting_after=<id>
    threshold = 0 if starting_after is None else starting_after  # => None means "from the beginning"
    window = [r for r in ROWS if r > threshold][:limit]  # => co-05: an indexed WHERE on the last-seen key, then LIMIT
    next_cursor = window[-1] if len(window) == limit and window[-1] != ROWS[-1] else None  # => None at the very end
    return Page(data=window, next_cursor=next_cursor)  # => the page + the cursor the NEXT request uses


first = page_starting_after(starting_after=None, limit=10)  # => page 1: ids 1..10
print(f"page 1: first={first.data[0]}, last={first.data[-1]}, next_cursor={first.next_cursor}")  # => Output: 1, 10, 10

second = page_starting_after(starting_after=first.next_cursor, limit=10)  # => resumes right after id 10
print(f"page 2: first={second.data[0]}, last={second.data[-1]}, next_cursor={second.next_cursor}")  # => Output: 11, 20, 20

assert second.data[0] == 11  # => co-05: the next page begins right AFTER the cursor id, no skip cost
assert first.data + second.data == list(range(1, 21))  # => contiguous, no overlap and no gap
```

**Run**: `python3 example.py`

**Output**:

```text
page 1: first=1, last=10, next_cursor=10
page 2: first=11, last=20, next_cursor=20
```

**Key takeaway**: A cursor resumes from a position in the data, not a raw row count -- so the next page begins right after the cursor id.

**Why it matters**: Keyset paging avoids the fetch-and-discard cost and is the correct default for a production list endpoint.

---

### Example 14: Cursor Stability Under Concurrent Insert

_ex-14 &middot; exercises co-05_

Because a cursor anchors to a position IN THE DATA, it is unaffected by a row inserted before the next page. An equivalent OFFSET page drifts -- it skips or repeats a row.

**`learning/code/ex-14-cursor-stable-under-insert/example.py`**

```python
# pyright: strict
"""Example 14: Cursor Stability Under Concurrent Insert. (co-05)

Because a cursor anchors to a position IN THE DATA (the last-seen id), it is
unaffected by a row inserted BEFORE the next page. An equivalent OFFSET page
DRIFTS: a new row near the front shifts every later position, so the offset
page either skips or repeats a row. Source: "Use The Index, Luke -- No Offset".
"""

ROWS = list(range(1, 11))  # => 10 rows, ids 1..10 (mutated below by a mid-scan insert)


def page_cursor(rows: list[int], starting_after: int | None, limit: int) -> list[int]:
    threshold = 0 if starting_after is None else starting_after  # => resume point IN the data
    return [r for r in rows if r > threshold][:limit]  # => co-05: WHERE id > cursor, stable under inserts


def page_offset(rows: list[int], offset: int, limit: int) -> list[int]:
    return rows[offset : offset + limit]  # => co-04: raw position -- drifts if rows shift


# Take the first page (ids 1..3), establishing a cursor/offset at id 3.
first_cursor = page_cursor(ROWS, None, 3)  # => [1, 2, 3]
first_offset = page_offset(ROWS, 0, 3)  # => [1, 2, 3]
print(f"page 1 (cursor): {first_cursor}")  # => Output: [1, 2, 3]
print(f"page 1 (offset): {first_offset}")  # => Output: [1, 2, 3]

# A new row is inserted at the FRONT of the list mid-scan (simulating a concurrent insert).
ROWS.insert(0, 0)  # => now [0, 1, 2, ..., 10] -- a row landed near the front

next_cursor = page_cursor(ROWS, starting_after=3, limit=3)  # => co-05: WHERE id > 3 -> [4, 5, 6] (unaffected)
next_offset = page_offset(ROWS, offset=3, limit=3)  # => co-04: position 3 shifted -> [3, 4, 5] (REPEATS id 3)
print(f"page 2 (cursor), after insert: {next_cursor}")  # => Output: [4, 5, 6] -- stable, no repeat
print(f"page 2 (offset), after insert: {next_offset}")  # => Output: [3, 4, 5] -- DRIFTED, id 3 repeated

assert next_cursor == [4, 5, 6]  # => co-05: cursor page is unaffected by the insert
assert 3 in next_offset and 3 not in next_cursor  # => co-04: offset page repeated id 3; cursor did not
```

**Run**: `python3 example.py`

**Output**:

```text
page 1 (cursor): [1, 2, 3]
page 1 (offset): [1, 2, 3]
page 2 (cursor), after insert: [4, 5, 6]
page 2 (offset), after insert: [3, 4, 5]
```

**Key takeaway**: A cursor is stable under concurrent writes; an offset page drifts because a new row shifts every later position.

**Why it matters**: This drift is the concrete reason cursor pagination wins at any real scale where inserts happen mid-scan.

---

### Example 15: Idempotency-Key -- Store and Replay

_ex-15 &middot; exercises co-06_

On a first POST the server records key -> response. A REPLAY of the same key returns the ORIGINAL stored response (200) instead of creating a second resource -- Stripe prior art; the IETF draft lapsed.

**`learning/code/ex-15-idempotency-key-store/example.py`**

```python
# pyright: strict
"""Example 15: Idempotency-Key -- store and replay. (co-06)

On a first POST the server records key -> response. A REPLAY of the same key
returns the ORIGINAL stored response (200) instead of creating a second
resource. This is Stripe's own prior art: store the first result under the
key, replay returns it -- even a 500. NOTE: the IETF draft
(draft-ietf-httpapi-idempotency-key-header-07) is EXPIRED/lapsed, not an RFC,
so this example follows Stripe prior art, not a lapsed draft.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-06: the response shape stored and replayed
class Response:
    status: int  # => 201 on first create, 200 on replay
    body: dict[str, object] = field(default_factory=dict[str, object])  # => the resource representation


STORE: dict[int, dict[str, object]] = {}  # => the resource store
IDEMPOTENCY_STORE: dict[str, dict[str, object]] = {}  # => co-06: key -> the BODY the first call produced
NEXT_ID = [1]  # => a mutable counter cell


def create_order(idempotency_key: str, item: str) -> Response:  # => POST /orders -- idempotent via key
    if idempotency_key in IDEMPOTENCY_STORE:  # => co-06: a REPLAY -- do NOT create a second order
        return Response(status=200, body=IDEMPOTENCY_STORE[idempotency_key])  # => returns the ORIGINAL body, 200 semantics
    new_id = NEXT_ID[0]  # => a fresh id for a genuinely new order
    order: dict[str, object] = {"id": new_id, "item": item}  # => the new resource
    STORE[new_id] = order  # => persists it
    IDEMPOTENCY_STORE[idempotency_key] = order  # => co-06: recorded so a future replay is safe
    NEXT_ID[0] += 1  # => advances the counter for the next genuinely new order
    return Response(status=201, body=order)  # => 201 on first create


first = create_order("client-key-A", "Widget")  # => a genuinely new key -> creates
print(f"first call:  status={first.status}, body={first.body}")  # => Output: 201, id=1

replay = create_order("client-key-A", "Widget")  # => co-06: SAME key -> returns the ORIGINAL response
print(f"replay call: status={replay.status}, body={replay.body}")  # => Output: 200, SAME id=1

assert first.status == 201 and replay.status == 200  # => co-06: first 201, replay 200
assert first.body == replay.body  # => the replay returns the IDENTICAL response
assert len(STORE) == 1  # => only ONE order was created across both calls
```

**Run**: `python3 example.py`

**Output**:

```text
first call:  status=201, body={'id': 1, 'item': 'Widget'}
replay call: status=200, body={'id': 1, 'item': 'Widget'}
```

**Key takeaway**: A known key short-circuits to the ORIGINAL response, so a retried POST creates nothing new.

**Why it matters**: This is the explicit mechanism that makes a non-idempotent method (POST) safely retryable.

---

### Example 16: Idempotency-Key -- a Retried Charge Applies Once

_ex-16 &middot; exercises co-06_

A retried POST charge with the SAME Idempotency-Key must not double-charge. The first call debits and records the key; a replay returns the original result WITHOUT debiting again.

**`learning/code/ex-16-idempotency-key-no-double-apply/example.py`**

```python
# pyright: strict
"""Example 16: Idempotency-Key -- a retried charge applies ONCE. (co-06)

A retried POST charge with the SAME Idempotency-Key must not double-charge.
This example models a wallet balance: the first call debits and records the
key; a replay returns the original result WITHOUT debiting again.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-06: the charge result stored and replayed
class ChargeResult:
    status: int  # => 201 first, 200 replay
    body: dict[str, object] = field(default_factory=dict[str, object])  # => charge id + new balance


BALANCE = [1000]  # => the wallet, mutable so a debit persists across calls
CHARGES: dict[str, dict[str, object]] = {}  # => co-06: idempotency key -> the charge BODY


def charge(idempotency_key: str, amount: int) -> ChargeResult:  # => POST /charges -- debit the wallet
    if idempotency_key in CHARGES:  # => co-06: a REPLAY -> return original body, do NOT debit again
        return ChargeResult(status=200, body=CHARGES[idempotency_key])  # => the original result, untouched
    BALANCE[0] -= amount  # => genuinely new charge -> debit the wallet once
    body: dict[str, object] = {"charged": amount, "balance": BALANCE[0]}  # => the result body
    CHARGES[idempotency_key] = body  # => co-06: recorded so a replay is a no-op
    return ChargeResult(status=201, body=body)  # => 201 on the genuine charge


first = charge("pay-key-1", 250)  # => genuine charge: 1000 -> 750
print(f"first charge:  status={first.status}, body={first.body}")  # => Output: 201, balance 750

replay = charge("pay-key-1", 250)  # => co-06: retry after a timeout -- SAME key, no second debit
print(f"replay charge: status={replay.status}, body={replay.body}")  # => Output: 200, balance still 750

second = charge("pay-key-2", 100)  # => a DIFFERENT key -> a genuinely new charge
print(f"second charge: status={second.status}, body={second.body}")  # => Output: 201, balance 650

assert BALANCE[0] == 650  # => co-06: debited exactly 250 + 100 = 350, the replay did NOT double-charge
assert first.body["balance"] == replay.body["balance"]  # => replay returned the original result unchanged
```

**Run**: `python3 example.py`

**Output**:

```text
first charge:  status=201, body={'charged': 250, 'balance': 750}
replay charge: status=200, body={'charged': 250, 'balance': 750}
second charge: status=201, body={'charged': 100, 'balance': 650}
```

**Key takeaway**: The balance is debited exactly once across the original charge and its replay -- no double-apply.

**Why it matters**: Idempotency keys came from payments (a retried charge must not double-bill), the canonical motivating use case.

---

### Example 17: Idempotency-Key Mismatch -- Reused with a Different Body

_ex-17 &middot; exercises co-06_

Reusing a known key with a DIFFERENT request body is a client bug. The server REJECTS it rather than silently returning the stale response or applying the new body.

**`learning/code/ex-17-idempotency-key-mismatch/example.py`**

```python
# pyright: strict
"""Example 17: Idempotency-Key Mismatch -- reuse a key with a different body. (co-06)

Reusing a known key with a DIFFERENT request body is a client bug (not a safe
retry). The server REJECTS it rather than silently returning the stale
response or applying the new body. This prevents a key collision from doing
the wrong thing on either side.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-06: status plus body or error
class Response:
    status: int  # => the HTTP status code
    body: dict[str, object] = field(default_factory=dict[str, object])  # => resource or error payload


STORE: dict[int, dict[str, object]] = {}  # => the resource store
IDEMPOTENCY_STORE: dict[str, tuple[str, Response]] = {}  # => co-06: key -> (request body hash, response)
NEXT_ID = [1]  # => a mutable counter cell


def create_order(idempotency_key: str, item: str) -> Response:  # => POST /orders -- idempotent + mismatch-checked
    if idempotency_key in IDEMPOTENCY_STORE:  # => key was seen before -- inspect whether the body matches
        seen_body, stored_response = IDEMPOTENCY_STORE[idempotency_key]  # => the original body + response
        if seen_body != item:  # => co-06: SAME key, DIFFERENT body -> client bug, REJECT
            return Response(409, {"error": "idempotency key reused with a different body"})  # => 409, rejected
        return stored_response  # => identical body -> safe replay, return the original
    new_id = NEXT_ID[0]  # => a fresh id for a genuinely new order
    order: dict[str, object] = {"id": new_id, "item": item}  # => the new resource
    STORE[new_id] = order  # => persists it
    response = Response(201, order)  # => the first-call response
    IDEMPOTENCY_STORE[idempotency_key] = (item, response)  # => co-06: record body + response together
    NEXT_ID[0] += 1  # => advances the counter
    return response  # => 201 on first create


first = create_order("key-X", "Widget")  # => genuine new order
print(f"first (Widget):    status={first.status}, body={first.body}")  # => Output: 201, id=1

safe_replay = create_order("key-X", "Widget")  # => SAME key, SAME body -> safe replay
print(f"replay (Widget):   status={safe_replay.status}, body={safe_replay.body}")  # => Output: 200, id=1

mismatch = create_order("key-X", "Gadget")  # => co-06: SAME key, DIFFERENT body -> REJECTED
print(f"mismatch (Gadget): status={mismatch.status}, body={mismatch.body}")  # => Output: 409, rejected

assert first.status == 201 and safe_replay.body == first.body  # => genuine + safe replay
assert mismatch.status == 409  # => co-06: a mismatched reuse is rejected, never applied
assert len(STORE) == 1  # => still only one order -- the mismatch created nothing
```

**Run**: `python3 example.py`

**Output**:

```text
first (Widget):    status=201, body={'id': 1, 'item': 'Widget'}
replay (Widget):   status=201, body={'id': 1, 'item': 'Widget'}
mismatch (Gadget): status=409, body={'error': 'idempotency key reused with a different body'}
```

**Key takeaway**: A reused key with a different body is rejected -- it's a client bug, not a safe retry.

**Why it matters**: Rejecting on mismatch prevents a key collision from doing the wrong thing on either side.

---

### Example 18: Repository -- a Collection-Like Interface

_ex-18 &middot; exercises co-09_

A Repository mediates between the domain and the data store, exposing a collection-like interface (add/get/all/remove) so the domain never touches the storage mechanism (Fowler, PoEAA).

**`learning/code/ex-18-repository-crud/example.py`**

```python
# pyright: strict
"""Example 18: Repository -- a collection-like interface over a store. (co-09)

A Repository mediates between the domain and the data store, exposing a
COLLECTION-LIKE interface (add/get/all/remove) so the domain never touches
the storage mechanism directly. Source: Martin Fowler, PoEAA -- "a
collection-like interface for accessing domain objects."
"""

from dataclasses import dataclass  # => a small typed domain object


@dataclass  # => the domain object this repository holds
class Task:
    id: int  # => the resource identifier
    title: str  # => the resource's own data


class TaskRepository:  # => co-09: a collection-like interface over an in-memory store
    def __init__(self) -> None:
        self._store: dict[int, Task] = {}  # => the private storage; callers never touch this
        self._next_id = 1  # => the id minted by the NEXT add()

    def add(self, title: str) -> Task:  # => add one member to the collection
        task = Task(id=self._next_id, title=title)  # => a new domain object
        self._store[task.id] = task  # => persists it
        self._next_id += 1  # => advances the id counter
        return task  # => returns the added member

    def get(self, task_id: int) -> Task | None:  # => fetch one member by id
        return self._store.get(task_id)  # => None when absent -- a collection's "not found"

    def all(self) -> list[Task]:  # => the whole collection
        return list(self._store.values())  # => a snapshot list, decoupled from internal storage

    def remove(self, task_id: int) -> bool:  # => remove one member
        if task_id in self._store:  # => present -> delete and report success
            del self._store[task_id]  # => removes the member
            return True  # => removed
        return False  # => nothing to remove


repo = TaskRepository()  # => co-09: the domain talks to THIS, not to a dict directly
created = repo.add("Write docs")  # => CREATE through the collection interface
repo.add("Ship release")  # => a second member
print(f"get(1): {repo.get(1)}")  # => Output: Task(id=1, title='Write docs')
print(f"all():  {repo.all()}")  # => Output: both tasks
print(f"remove(1): {repo.remove(1)}")  # => Output: True
print(f"get(1) after remove: {repo.get(1)}")  # => Output: None -- gone from the collection

assert repo.get(1) is None and len(repo.all()) == 1  # => co-09: full CRUD round-trip through the repository
```

**Run**: `python3 example.py`

**Output**:

```text
get(1): Task(id=1, title='Write docs')
all():  [Task(id=1, title='Write docs'), Task(id=2, title='Ship release')]
remove(1): True
get(1) after remove: None
```

**Key takeaway**: The domain talks to a collection interface (add/get/all/remove), not a dict or a table.

**Why it matters**: Decoupling the domain from storage is what lets the backend be swapped without touching domain logic.

---

### Example 19: Repository -- Swap the Backend, Callers Unchanged

_ex-19 &middot; exercises co-09_

Two implementations (an in-memory dict and a 'sql-like' list-backed one) both satisfy the SAME protocol, so the domain code that uses them never changes when the backend is swapped.

**`learning/code/ex-19-repository-swap-backend/example.py`**

```python
# pyright: strict
"""Example 19: Repository -- swap the backend, callers unchanged. (co-09)

A Repository is an ABSTRACTION over storage. Two implementations (an in-
memory dict and a "sql-like" list-backed one) both satisfy the SAME protocol,
so the domain code that uses them never changes when the backend is swapped.
"""

from dataclasses import dataclass  # => a small typed domain object
from typing import Protocol  # => Protocol: a structural interface both backends satisfy


@dataclass  # => the domain object
class Task:
    id: int  # => the resource identifier
    title: str  # => the resource's own data


class TaskRepository(Protocol):  # => co-09: the collection-like interface BOTH backends implement
    def add(self, title: str) -> Task: ...  # => add one member
    def all(self) -> list[Task]: ...  # => the whole collection


class InMemoryRepo:  # => co-09: backend 1 -- a dict
    def __init__(self) -> None:
        self._store: dict[int, Task] = {}  # => dict-backed storage
        self._next = 1  # => the next id

    def add(self, title: str) -> Task:
        task = Task(self._next, title)  # => builds the domain object
        self._store[task.id] = task  # => persists in a dict
        self._next += 1  # => advances the id
        return task  # => returns the added member

    def all(self) -> list[Task]:
        return list(self._store.values())  # => snapshot of the dict


class ListBackedRepo:  # => co-09: backend 2 -- a "sql-like" list of rows
    def __init__(self) -> None:
        self._rows: list[Task] = []  # => list-backed storage (stands in for a SQL table)

    def add(self, title: str) -> Task:
        next_id = (max((t.id for t in self._rows), default=0)) + 1  # => derives the next id from existing rows
        task = Task(next_id, title)  # => builds the domain object
        self._rows.append(task)  # => appends a row (stands in for an INSERT)
        return task  # => returns the added member

    def all(self) -> list[Task]:
        return list(self._rows)  # => snapshot of the list


def use(repo: TaskRepository) -> None:  # => co-09: domain code that depends on the PROTOCOL, not a backend
    repo.add("Shared task A")  # => add through the interface
    repo.add("Shared task B")  # => add through the interface
    print(f"  members: {[t.title for t in repo.all()]}")  # => Output: both tasks, regardless of backend


print("InMemoryRepo:")  # => Output: header for backend 1
use(InMemoryRepo())  # => co-09: callers unchanged
print("ListBackedRepo:")  # => Output: header for backend 2
use(ListBackedRepo())  # => co-09: SAME domain code, DIFFERENT backend

# The domain `use()` function references ONLY the protocol -- swapping the backend changed nothing in it.
```

**Run**: `python3 example.py`

**Output**:

```text
InMemoryRepo:
  members: ['Shared task A', 'Shared task B']
ListBackedRepo:
  members: ['Shared task A', 'Shared task B']
```

**Key takeaway**: Same protocol, two backends -- the domain code referencing the protocol is unchanged by the swap.

**Why it matters**: This is the practical payoff of the repository abstraction: persistence is pluggable.

---

### Example 20: Unit of Work -- Track Changes, Commit Once

_ex-20 &middot; exercises co-10_

A Unit of Work maintains a list of objects affected by a business transaction and coordinates writing them out -- all changes commit together on commit() (Fowler, PoEAA).

**`learning/code/ex-20-unit-of-work-commit/example.py`**

```python
# pyright: strict
"""Example 20: Unit of Work -- track changes, commit once. (co-10)

A Unit of Work maintains a list of objects affected by a business transaction
and coordinates writing them out -- all changes commit together on commit().
Source: Martin Fowler, PoEAA -- Unit of Work pattern.
"""

from dataclasses import dataclass  # => a small typed domain object


@dataclass  # => the domain object; mutated in memory, flushed by the UoW
class Task:
    id: int  # => the resource identifier
    title: str  # => mutated during the transaction


@dataclass  # => co-10: a fully-typed snapshot of everything commit() writes out, together
class Flush:
    inserted: list[dict[str, object]]  # => the new objects, serialized
    updated: list[dict[str, object]]  # => the modified objects, serialized
    deleted_ids: list[int]  # => the removed ids


class UnitOfWork:  # => co-10: tracks the objects changed in one business transaction
    def __init__(self) -> None:
        self._new: list[Task] = []  # => objects to INSERT on commit
        self._dirty: list[Task] = []  # => objects to UPDATE on commit
        self._deleted_ids: list[int] = []  # => object ids to DELETE on commit
        self.committed = False  # => whether commit() has run

    def register_new(self, task: Task) -> None:  # => track a brand-new object
        self._new.append(task)  # => queued for INSERT

    def register_dirty(self, task: Task) -> None:  # => track a modified existing object
        self._dirty.append(task)  # => queued for UPDATE

    def register_deleted(self, task_id: int) -> None:  # => track a removal
        self._deleted_ids.append(task_id)  # => queued for DELETE

    def commit(self) -> Flush:  # => co-10: write ALL tracked changes out, together
        flush = Flush(  # => one coordinated write-out of every change
            inserted=[t.__dict__ for t in self._new],  # => the new objects, serialized
            updated=[t.__dict__ for t in self._dirty],  # => the modified objects, serialized
            deleted_ids=list(self._deleted_ids),  # => the removed ids
        )
        self.committed = True  # => the transaction is now durably written
        return flush  # => the single, coordinated result


uow = UnitOfWork()  # => co-10: open a business transaction
uow.register_new(Task(id=1, title="New task"))  # => stage an INSERT (not written yet)
existing = Task(id=2, title="old")  # => an existing object loaded into the transaction
existing.title = "updated"  # => mutate it in memory
uow.register_dirty(existing)  # => stage an UPDATE (not written yet)
uow.register_deleted(7)  # => stage a DELETE (not written yet)
print(f"committed before commit(): {uow.committed}")  # => Output: False -- nothing written yet

flush = uow.commit()  # => co-10: ALL three changes land TOGETHER in one write-out
print(f"flush: {flush}")  # => Output: inserted + updated + deleted, all at once

assert uow.committed is True  # => co-10: the transaction committed
assert len(flush.inserted) == 1 and len(flush.updated) == 1 and flush.deleted_ids == [7]  # => all three changes landed
```

**Run**: `python3 example.py`

**Output**:

```text
committed before commit(): False
flush: Flush(inserted=[{'id': 1, 'title': 'New task'}], updated=[{'id': 2, 'title': 'updated'}], deleted_ids=[7])
```

**Key takeaway**: A UoW stages every change and writes them ALL out together on commit(), not piecemeal.

**Why it matters**: Staging changes is the precondition for the atomic-commit boundary (co-11).

---

### Example 21: Unit of Work -- Rollback Discards Tracked Changes

_ex-21 &middot; exercises co-10, co-11_

Rolling back a Unit of Work throws away EVERY staged change: nothing the transaction registered is written out. This is the atomic-commit boundary from the discard side.

**`learning/code/ex-21-unit-of-work-rollback/example.py`**

```python
# pyright: strict
"""Example 21: Unit of Work -- rollback discards tracked changes. (co-10, co-11)

Rolling back a Unit of Work throws away EVERY staged change: nothing the
transaction registered is written out. This is the atomic-commit boundary
(co-11) from the discard side -- either everything commits, or nothing does.
"""

from dataclasses import dataclass  # => a small typed domain object


@dataclass  # => the domain object staged in the transaction
class Task:
    id: int  # => the resource identifier
    title: str  # => the resource's own data


STORE: dict[int, Task] = {1: Task(1, "persistent")}  # => the durable store -- rollback must leave it untouched


class UnitOfWork:  # => co-10: a staging area for one business transaction
    def __init__(self, store: dict[int, Task]) -> None:
        self._store = store  # => the durable backing store
        self._pending: list[Task] = []  # => staged changes, NOT yet written

    def register_new(self, task: Task) -> None:  # => stage an insert
        self._pending.append(task)  # => queued, not yet visible in the store

    def commit(self) -> None:  # => co-10: write every staged change into the store
        for task in self._pending:  # => flush each staged object
            self._store[task.id] = task  # => durably written

    def rollback(self) -> None:  # => co-10/co-11: discard ALL staged changes
        self._pending.clear()  # => nothing staged is ever written -- the store is untouched


uow = UnitOfWork(STORE)  # => open a transaction over the durable store
uow.register_new(Task(2, "ephemeral"))  # => stage a change -- NOT yet in STORE
print(f"store before rollback: { {k: v.title for k, v in STORE.items()} }")  # => Output: only id 1

uow.rollback()  # => co-10/co-11: discard -- the staged task is gone
print(f"store after rollback:  { {k: v.title for k, v in STORE.items()} }")  # => Output: still only id 1

assert 2 not in STORE and STORE[1].title == "persistent"  # => co-11: no tracked change persisted after rollback
```

**Run**: `python3 example.py`

**Output**:

```text
store before rollback: {1: 'persistent'}
store after rollback:  {1: 'persistent'}
```

**Key takeaway**: Rollback discards every staged change -- the durable store is untouched.

**Why it matters**: Either everything commits or nothing does -- the ACID atomicity guarantee.

---

### Example 22: Transaction Atomicity -- All Commit or All Roll Back

_ex-22 &middot; exercises co-11_

Two writes inside one transaction: when both succeed they commit together; when a failure occurs MID-transaction, both roll back and neither survives.

**`learning/code/ex-22-transaction-atomic/example.py`**

```python
# pyright: strict
"""Example 22: Transaction Atomicity -- all commit or all roll back. (co-11)

Two writes inside one transaction: when both succeed they commit together;
when a failure occurs MID-transaction, both roll back and neither write
survives. This is the ACID atomicity guarantee -- an all-or-nothing commit
boundary.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => a typed account -- avoids dict[str, str|int] inference problems
class Account:
    name: str  # => the account label (for readable write descriptions)
    balance: int  # => the balance mutated inside the transaction


@dataclass  # => co-11: a transaction collects writes and commits or rolls them back atomically
class Transaction:
    writes: list[str] = field(default_factory=list[str])  # => staged writes, in order
    committed: bool = False  # => whether the transaction reached commit


def transfer(from_account: Account, to_account: Account, amount: int) -> Transaction:
    # => co-11: two writes (debit + credit) that must be ATOMIC
    tx = Transaction()  # => open the transaction
    tx.writes.append(f"debit {from_account.name} {amount}")  # => stage write 1: debit
    if from_account.balance < amount:  # => a mid-transaction FAILURE (insufficient funds)
        return tx  # => co-11: rollback -- neither write is committed (committed stays False)
    from_account.balance -= amount  # => apply write 1
    tx.writes.append(f"credit {to_account.name} {amount}")  # => stage write 2: credit
    to_account.balance += amount  # => apply write 2
    tx.committed = True  # => co-11: both writes succeeded -> commit atomically
    return tx  # => the committed transaction


# Case A: enough funds -> both writes commit together.
alice = Account("alice", 100)  # => account 1
bob = Account("bob", 50)  # => account 2
ok = transfer(alice, bob, 30)  # => co-11: both writes land
print(f"success: committed={ok.committed}, alice={alice.balance}, bob={bob.balance}")  # => Output: True, 70, 80
print(f"  writes: {ok.writes}")  # => Output: both debit and credit

# Case B: insufficient funds -> failure mid-transaction -> both roll back.
carol = Account("carol", 10)  # => account with too little
dave = Account("dave", 0)  # => account 2
failed = transfer(carol, dave, 500)  # => co-11: fails after staging the debit -> rollback
print(f"failure: committed={failed.committed}, carol={carol.balance}, dave={dave.balance}")  # => Output: False, 10, 0
print(f"  writes: {failed.writes}")  # => Output: only the staged debit (never applied/committed)

assert ok.committed and alice.balance == 70 and bob.balance == 80  # => co-11: success committed both
assert not failed.committed and carol.balance == 10 and dave.balance == 0  # => co-11: failure rolled both back
```

**Run**: `python3 example.py`

**Output**:

```text
success: committed=True, alice=70, bob=80
  writes: ['debit alice 30', 'credit bob 30']
failure: committed=False, carol=10, dave=0
  writes: ['debit carol 500']
```

**Key takeaway**: A debit and a credit commit together, or both roll back -- never half-applied.

**Why it matters**: Atomicity is what makes a multi-step business operation all-or-nothing instead of leaving the books unbalanced.

---

### Example 23: JWT -- Encode, Sign, and Verify

_ex-23 &middot; exercises co-14_

A JWT is a signed, self-contained claims token (RFC 7519): header.payload.signature, base64url-encoded, signed with HMAC-SHA256. The receiver verifies the signature WITHOUT a session lookup.

**`learning/code/ex-23-jwt-encode-decode/example.py`**

```python
# pyright: strict
"""Example 23: JWT -- encode, sign, and verify (HS256, hand-rolled). (co-14)

A JWT is a signed, self-contained claims token (RFC 7519): header.payload.
signature, base64url-encoded, signed with HMAC-SHA256. The receiver verifies
the signature WITHOUT a session lookup -- the token itself carries the claims.
"""

import base64  # => stdlib: base64url encoding for each JWT segment
import hashlib  # => stdlib: SHA-256 for the HMAC
import hmac  # => stdlib: HMAC-SHA256 signing + constant-time compare
import json  # => stdlib: serialize the header and claims to compact JSON

SECRET = b"super-secret-key"  # => the HMAC shared secret (in production, loaded from env, never hardcoded in source shipped to a client)


def b64url(raw: bytes) -> str:  # => base64url-encode WITHOUT "=" padding (the JWT segment format)
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")  # => strips padding per RFC 7515


def sign(message: bytes) -> str:  # => HMAC-SHA256, then base64url -- the JWT signature segment
    return b64url(hmac.new(SECRET, message, hashlib.sha256).digest())  # => keyed hash over header.payload


def encode(claims: dict[str, object]) -> str:  # => co-14: build a signed compact JWT
    header = b64url(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())  # => segment 1: header
    payload = b64url(json.dumps(claims, separators=(",", ":")).encode())  # => segment 2: claims
    signing_input = f"{header}.{payload}".encode()  # => the bytes the signature covers
    signature = sign(signing_input)  # => segment 3: signature
    return f"{header}.{payload}.{signature}"  # => the compact serialised JWT


def verify(token: str) -> dict[str, object] | None:  # => co-14: verify signature + return claims, or None on tamper
    try:
        header_b64, payload_b64, signature = token.split(".")  # => the three segments
    except ValueError:  # => not three segments -> malformed
        return None  # => reject
    expected = sign(f"{header_b64}.{payload_b64}".encode())  # => recompute the signature over the same input
    if not hmac.compare_digest(expected, signature):  # => co-14: constant-time compare; mismatch -> tampered
        return None  # => reject
    raw = base64.urlsafe_b64decode(payload_b64 + "==")  # => re-pad before decoding the payload
    return json.loads(raw)  # => the verified claims


token = encode({"sub": "user-42", "role": "admin"})  # => co-14: issue a signed token
print(f"token: {token[:48]}...")  # => Output: a prefix of the compact JWT (truncated for display)

claims = verify(token)  # => co-14: verify + decode -- no session lookup needed
print(f"verified claims: {claims}")  # => Output: {'sub': 'user-42', 'role': 'admin'}

tampered = token[:-2] + ("AA" if not token.endswith("AA") else "BB")  # => corrupt the signature segment
print(f"tampered verifies: {verify(tampered)}")  # => Output: None -- signature mismatch rejected

assert claims == {"sub": "user-42", "role": "admin"}  # => co-14: round-trip succeeds
assert verify(tampered) is None  # => co-14: a tampered token is rejected
```

**Run**: `python3 example.py`

**Output**:

```text
token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ...
verified claims: {'sub': 'user-42', 'role': 'admin'}
tampered verifies: None
```

**Key takeaway**: A JWT is verified by recomputing the HMAC over header.payload -- no session store needed.

**Why it matters**: A tampered token is rejected because its signature no longer matches -- stateless verification.

---

### Example 24: JWT -- an Expired Token Is Rejected

_ex-24 &middot; exercises co-14_

A JWT carries an exp (expiry) claim: the receiver rejects any token whose exp is in the past, limiting a stolen token's lifetime.

**`learning/code/ex-24-jwt-expiry/example.py`**

```python
# pyright: strict
"""Example 24: JWT -- an expired token is rejected. (co-14)

A JWT carries an `exp` (expiry) claim: the receiver rejects any token whose
exp is in the past. This is how short-lived tokens limit the blast radius of a
stolen token. Source: RFC 7519 Sec 4.1.4 (`exp`).
"""

import base64  # => stdlib: base64url segment encoding
import hashlib  # => stdlib: SHA-256 for the HMAC
import hmac  # => stdlib: HMAC-SHA256 signing
import json  # => stdlib: serialize header and claims


SECRET = b"super-secret-key"  # => the HMAC shared secret


def b64url(raw: bytes) -> str:  # => base64url without padding
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")  # => JWT segment format


def sign(message: bytes) -> str:  # => HMAC-SHA256 -> base64url
    return b64url(hmac.new(SECRET, message, hashlib.sha256).digest())  # => keyed hash


def encode(claims: dict[str, object]) -> str:  # => build a signed compact JWT
    header = b64url(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())  # => header segment
    payload = b64url(json.dumps(claims, separators=(",", ":")).encode())  # => claims segment
    return f"{header}.{payload}.{sign(f'{header}.{payload}'.encode())}"  # => compact JWT


def verify(token: str, now: int) -> dict[str, object] | None:  # => co-14: signature + expiry check
    header_b64, payload_b64, signature = token.split(".")  # => the three segments
    if not hmac.compare_digest(sign(f"{header_b64}.{payload_b64}".encode()), signature):  # => signature mismatch
        return None  # => reject
    claims: dict[str, object] = json.loads(base64.urlsafe_b64decode(payload_b64 + "=="))  # => decode claims
    exp = claims.get("exp")  # => co-14: the expiry timestamp
    if isinstance(exp, int) and now >= exp:  # => co-14: `now` is AT/AFTER exp -> token expired
        return None  # => reject -- the token's lifetime is over
    return claims  # => fresh enough -> valid


fresh = encode({"sub": "user-1", "exp": 2000})  # => a token expiring at t=2000
expired = encode({"sub": "user-1", "exp": 1000})  # => a token that already expired at t=1000

print(f"fresh at now=1500:   {verify(fresh, now=1500)}")  # => Output: claims -- now < exp
print(f"expired at now=1500: {verify(expired, now=1500)}")  # => Output: None -- now >= exp

assert verify(fresh, now=1500) is not None  # => co-14: a not-yet-expired token passes
assert verify(expired, now=1500) is None  # => co-14: an expired token is rejected
```

**Run**: `python3 example.py`

**Output**:

```text
fresh at now=1500:   {'sub': 'user-1', 'exp': 2000}
expired at now=1500: None
```

**Key takeaway**: An expired token (now >= exp) is rejected, even though its signature is still valid.

**Why it matters**: Short-lived tokens cap the blast radius of a stolen credential.

---

### Example 25: RBAC -- a Role-Restricted Route

_ex-25 &middot; exercises co-17_

Role-Based Access Control maps users -> roles -> privileges (the NIST model). A route demands a role; the right role is allowed (200), the wrong role is denied (403).

**`learning/code/ex-25-rbac-role-gate/example.py`**

```python
# pyright: strict
"""Example 25: RBAC -- a role-restricted route. (co-17)

Role-Based Access Control (RBAC) maps users -> roles -> privileges (the NIST
model, Ferraiolo & Kuhn 1992, INCITS 359). A route demands a role; a user
with the right role is allowed (200), a user with the wrong role is denied
(403). Source: NIST CSRC RBAC.
"""

from dataclasses import dataclass  # => a small typed response record


@dataclass  # => co-17: status plus a short message
class Response:
    status: int  # => 200 allowed, 403 forbidden
    body: dict[str, str]  # => a short message


# users -> role; the role -> the set of privileges it grants.
USERS: dict[str, str] = {"ada": "admin", "grace": "viewer"}  # => the user -> role mapping
ROLE_PRIVILEGES: dict[str, set[str]] = {"admin": {"billing:read", "billing:write"}, "viewer": {"billing:read"}}  # => role -> privileges


def view_billing(username: str) -> Response:  # => GET /billing -- requires billing:read
    role = USERS.get(username)  # => the user's role (None if unknown)
    privileges = ROLE_PRIVILEGES.get(role or "", set())  # => the privileges that role grants
    if "billing:read" not in privileges:  # => co-17: the role lacks the required privilege
        return Response(403, {"error": f"role {role!r} cannot read billing"})  # => 403
    return Response(200, {"billing": "ok", "viewed_by": username})  # => 200, allowed


admin = view_billing("ada")  # => role "admin" has billing:read
print(f"admin views billing:  status={admin.status}, body={admin.body}")  # => Output: 200

viewer = view_billing("grace")  # => role "viewer" ALSO has billing:read
print(f"viewer views billing: status={viewer.status}, body={viewer.body}")  # => Output: 200

# A write attempt needs billing:write, which "viewer" lacks -- the RBAC gate denies it.
def write_billing(username: str) -> Response:  # => POST /billing -- requires billing:write
    role = USERS.get(username)  # => the user's role
    privileges = ROLE_PRIVILEGES.get(role or "", set())  # => that role's privileges
    if "billing:write" not in privileges:  # => co-17: lacks the write privilege
        return Response(403, {"error": f"role {role!r} cannot write billing"})  # => 403
    return Response(200, {"written_by": username})  # => 200


viewer_write = write_billing("grace")  # => "viewer" lacks billing:write -> 403
print(f"viewer writes billing: status={viewer_write.status}, body={viewer_write.body}")  # => Output: 403

assert admin.status == 200 and viewer.status == 200  # => co-17: read allowed for both roles
assert write_billing("ada").status == 200 and viewer_write.status == 403  # => co-17: write gated by role
```

**Run**: `python3 example.py`

**Output**:

```text
admin views billing:  status=200, body={'billing': 'ok', 'viewed_by': 'ada'}
viewer views billing: status=200, body={'billing': 'ok', 'viewed_by': 'grace'}
viewer writes billing: status=403, body={'error': "role 'viewer' cannot write billing"}
```

**Key takeaway**: RBAC gates an operation by role -- the right role gets 200, the wrong role gets 403.

**Why it matters**: RBAC is auditable and coarse; ABAC (next) is flexible but harder to manage -- a real trade-off.

---

### Example 26: ABAC -- an Owner-Only Attribute Policy

_ex-26 &middot; exercises co-17_

Attribute-Based Access Control decides access from RULES over ATTRIBUTES (the requester's, the resource's). Here the policy is 'the requester must OWN the resource'.

**`learning/code/ex-26-abac-attribute-gate/example.py`**

```python
# pyright: strict
"""Example 26: ABAC -- an owner-only attribute policy. (co-17)

Attribute-Based Access Control (ABAC) decides access from RULES over
ATTRIBUTES (the requester's, the resource's, the environment's) rather than
a fixed role table. Here the policy is "the requester must OWN the resource"
-- flexible, but the rule set is harder to audit than RBAC. Source: NIST CSRC.
"""

from dataclasses import dataclass  # => a small typed domain + response record


@dataclass  # => the resource carries its OWN owner attribute -- the thing the policy reads
class Document:
    id: int  # => the resource identifier
    owner: str  # => co-17: an ATTRIBUTE of the resource -- who owns it


@dataclass  # => co-17: status plus a short message
class Response:
    status: int  # => 200 allowed, 403 denied
    body: dict[str, str]  # => a short message


DOCS: dict[int, Document] = {1: Document(1, "ada"), 2: Document(2, "grace")}  # => resources with owner attributes
REQUESTERS: dict[str, str] = {"ada-token": "ada", "grace-token": "grace"}  # => token -> requester identity attribute


def view_doc(token: str, doc_id: int) -> Response:  # => GET /docs/{id} -- the ABAC owner policy
    requester = REQUESTERS.get(token)  # => the requester's identity ATTRIBUTE
    if requester is None:  # => no identity attribute at all
        return Response(401, {"error": "unknown requester"})  # => 401
    doc = DOCS.get(doc_id)  # => the resource (with its owner attribute)
    if doc is None:  # => resource does not exist
        return Response(404, {"error": "not found"})  # => 404
    # co-17: the ABAC RULE -- requester attribute (identity) must EQUAL resource attribute (owner)
    if requester != doc.owner:  # => the rule evaluates to DENY -- a non-owner is rejected
        return Response(403, {"error": "only the owner may view"})  # => 403
    return Response(200, {"doc_id": str(doc_id), "viewed_by": requester})  # => 200, owner


owner = view_doc("ada-token", 1)  # => ada owns doc 1 -> allowed
print(f"owner views own doc:    status={owner.status}, body={owner.body}")  # => Output: 200

non_owner = view_doc("grace-token", 1)  # => grace does NOT own doc 1 -> denied by the attribute rule
print(f"non-owner views doc 1:  status={non_owner.status}, body={non_owner.body}")  # => Output: 403

assert owner.status == 200  # => co-17: the owner attribute matches -> allowed
assert non_owner.status == 403  # => co-17: a non-owner is denied by the rule (ABAC, not a role table)
```

**Run**: `python3 example.py`

**Output**:

```text
owner views own doc:    status=200, body={'doc_id': '1', 'viewed_by': 'ada'}
non-owner views doc 1:  status=403, body={'error': 'only the owner may view'}
```

**Key takeaway**: ABAC reads attributes (identity vs owner) and applies a rule -- flexible, but the rule set is harder to audit than a role table.

**Why it matters**: RBAC vs ABAC is a real trade-off: auditable-and-coarse vs flexible-and-complex.

---

### Example 27: Structured Logging -- a JSON Line with Typed Fields

_ex-27 &middot; exercises co-25_

A structured log is a machine-parseable JSON object with typed fields (timestamp, level, message, request_id) rather than free text.

**`learning/code/ex-27-structured-log-json/example.py`**

```python
# pyright: strict
"""Example 27: Structured Logging -- a JSON line with typed fields. (co-25)

A structured log is a machine-parseable JSON object with typed fields
(timestamp, level, message, request_id) rather than free text. This example
emits one such line and verifies it parses back to a dict with the expected
keys -- so a downstream log aggregator can index every field.
"""

import json  # => stdlib: serialize the record to a JSON line and parse it back


def log_json(level: str, message: str, request_id: str, timestamp: str = "2026-07-29T10:00:00Z") -> str:
    # => co-25: every field is a TYPED value, not interpolated prose
    record: dict[str, str] = {  # => the structured fields
        "timestamp": timestamp,  # => when the event happened (ISO-8601)
        "level": level,  # => severity: info/warn/error
        "message": message,  # => a short human-readable summary
        "request_id": request_id,  # => co-25: the correlation key tying this line to one request
    }
    return json.dumps(record)  # => one JSON line, ready for a log shipper to ingest


line = log_json(level="info", message="order created", request_id="req-abc-123")  # => emit one structured line
print(line)  # => Output: a single JSON object on one line

parsed = json.loads(line)  # => co-25: verify it round-trips into a parseable dict
print(f"parsed message: {parsed['message']}")  # => Output: order created

expected_keys = {"timestamp", "level", "message", "request_id"}  # => the typed fields every line carries
assert set(parsed.keys()) == expected_keys  # => co-25: the line parses with exactly these fields
assert parsed["level"] == "info" and parsed["request_id"] == "req-abc-123"  # => fields are typed values
```

**Run**: `python3 example.py`

**Output**:

```text
{"timestamp": "2026-07-29T10:00:00Z", "level": "info", "message": "order created", "request_id": "req-abc-123"}
parsed message: order created
```

**Key takeaway**: A structured log line is a JSON object with typed fields, so an aggregator can index every one.

**Why it matters**: Free-text logs are unparseable downstream; structured logs are queryable.

---

### Example 28: Correlation ID -- Thread One Id Through Every Log Line

_ex-28 &middot; exercises co-25_

A correlation (request) id is minted at the request boundary and carried on EVERY log line the request produces, so all of a request's lines group together across functions and services.

**`learning/code/ex-28-correlation-id/example.py`**

```python
# pyright: strict
"""Example 28: Correlation ID -- thread one id through every log line. (co-25)

A correlation (request) id is minted at the request boundary and carried on
EVERY log line the request produces, so all of a request's lines group
together in a log aggregator -- across functions, across services.
"""

import json  # => stdlib: each log line is a JSON object


LOG_BUFFER: list[str] = []  # => collects the request's lines, so we can inspect them together


def log(level: str, message: str, request_id: str) -> None:  # => co-25: every line carries the SAME request_id
    LOG_BUFFER.append(json.dumps({"level": level, "message": message, "request_id": request_id}))  # => stamped with the id


def handle_request(request_id: str) -> None:  # => a request's lifetime, all lines sharing the id
    log("info", "received request", request_id)  # => entry line, stamped
    validate(request_id)  # => a deeper function still threads the SAME id
    log("info", "request complete", request_id)  # => exit line, stamped


def validate(request_id: str) -> None:  # => a nested call -- still carries the id down
    log("debug", "validating payload", request_id)  # => co-25: the id propagates across function boundaries


handle_request("req-xyz-789")  # => one request, three lines, one shared id
for line in LOG_BUFFER:  # => print every line the request produced
    print(line)  # => Output: three JSON lines, all carrying request_id=req-xyz-789

parsed = [json.loads(line) for line in LOG_BUFFER]  # => parse them all back
all_carry_id = all(entry["request_id"] == "req-xyz-789" for entry in parsed)  # => co-25: every line carries the id
print(f"every line carries the correlation id: {all_carry_id}")  # => Output: True
assert all_carry_id and len(LOG_BUFFER) == 3  # => co-25: three lines, one shared id throughout
```

**Run**: `python3 example.py`

**Output**:

```text
{"level": "info", "message": "received request", "request_id": "req-xyz-789"}
{"level": "debug", "message": "validating payload", "request_id": "req-xyz-789"}
{"level": "info", "message": "request complete", "request_id": "req-xyz-789"}
every line carries the correlation id: True
```

**Key takeaway**: One id on every line groups a whole request's logs together in an aggregator.

**Why it matters**: Without a correlation id, a request's scattered log lines are impossible to reassemble.

---

← Previous: [Overview](./overview.md) · Next: [Intermediate Examples](./intermediate.md) →
