# pyright: strict
"""Capstone Step 1: versioned REST + cursor pagination + idempotency-key. (co-03, co-05, co-06)

Following the syllabus's ordered capstone spec, this handler implements
GET /v1/articles (cursor pagination) and POST /v1/articles (Idempotency-Key
handling), and verifies a replayed write with the SAME key does NOT
double-apply. This is the foundation Steps 2-4 build on.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories

STORE: dict[int, dict[str, object]] = {
    1: {"id": 1, "title": "Hello, Capstone"}
}  # => seed data
IDEMPOTENCY_STORE: dict[
    str, dict[str, object]
] = {}  # => co-06: key -> the body the first write produced
NEXT_ID = [2]  # => the next id after the seeded article


@dataclass  # => the response shape every handler returns
class Response:
    status: int  # => the HTTP status code
    headers: dict[str, str] = field(
        default_factory=dict[str, str]
    )  # => carries Location / RateLimit
    body: dict[str, object] = field(
        default_factory=dict[str, object]
    )  # => the resource or error payload


def list_articles_v1(
    after_cursor: int | None, limit: int
) -> Response:  # => GET /v1/articles (co-05)
    all_ids = sorted(STORE.keys())  # => a stable, deterministic order
    threshold = (
        0 if after_cursor is None else after_cursor
    )  # => co-05: resume AFTER the cursor id
    page_ids = [i for i in all_ids if i > threshold][
        :limit
    ]  # => co-05: an indexed WHERE + LIMIT
    end_cursor = (
        page_ids[-1] if page_ids else None
    )  # => the cursor the NEXT request resumes from
    return Response(
        200, body={"ids": page_ids, "next_cursor": end_cursor}
    )  # => paginated envelope


def create_article_v1(
    idempotency_key: str, title: str
) -> Response:  # => POST /v1/articles (co-06)
    if (
        idempotency_key in IDEMPOTENCY_STORE
    ):  # => co-06: a REPLAY -> return the ORIGINAL body
        return Response(
            200, body=IDEMPOTENCY_STORE[idempotency_key]
        )  # => 200, no second article
    new_id = NEXT_ID[0]  # => mint an id for a genuinely new article
    article: dict[str, object] = {"id": new_id, "title": title}  # => the new resource
    STORE[new_id] = article  # => persist
    IDEMPOTENCY_STORE[idempotency_key] = (
        article  # => co-06: record so a future replay is safe
    )
    NEXT_ID[0] += 1  # => advance
    return Response(
        201, headers={"Location": f"/v1/articles/{new_id}"}, body=article
    )  # => 201 + Location


before = len(STORE)  # => store size BEFORE any write
first = create_article_v1(
    "cap-key-1", "Capstone Article"
)  # => a genuinely new key -> creates
print(f"first write:  status={first.status}, body={first.body}")  # => Output: 201, id=2

replay = create_article_v1(
    "cap-key-1", "Capstone Article"
)  # => co-06: SAME key -> returns the ORIGINAL
print(
    f"replay:       status={replay.status}, body={replay.body}"
)  # => Output: 200, SAME id=2

did_not_double_apply = (
    len(STORE) == before + 1
)  # => co-06: exactly ONE new article across both calls
print(f"replay did not double-apply: {did_not_double_apply}")  # => Output: True

page = list_articles_v1(
    after_cursor=None, limit=10
)  # => co-05: list confirms the write is visible
print(
    f"list:         status={page.status}, body={page.body}"
)  # => Output: both articles

assert first.status == 201 and replay.status == 200  # => co-06: first 201, replay 200
assert did_not_double_apply  # => co-06: no double-apply
assert page.body["ids"] == [
    1,
    2,
]  # => co-05: cursor pagination returns both articles in order
