# pyright: strict
"""Capstone Step 2: rest.py -- implement the spec, with idempotency-key handling. (co-13, co-17, co-18)

Following `openapi.yaml`'s (Step 1) contract, this handler implements
GET /v1/articles (cursor pagination, co-17), POST /v1/articles
(idempotency-key handling, co-18), and GET /v1/articles/{id} (a
problem+json error on a miss) -- and verifies a replayed write with the
same key does NOT double-apply.
"""

from dataclasses import dataclass, field  # => field: default_factory for mutable dataclass defaults

STORE: dict[int, dict[str, object]] = {1: {"id": 1, "title": "Hello, Capstone"}}  # => co-09: seed data
IDEMPOTENCY_STORE: dict[str, dict[str, object]] = {}  # => co-18: key -> the response it produced
NEXT_ID = [2]  # => a mutable counter cell -- the next id after the seeded article


@dataclass  # => co-09: status, headers, and body -- the shape every response below shares
class Response:  # => matches openapi.yaml's own declared response envelope
    status: int  # => the HTTP status code
    headers: dict[str, str] = field(default_factory=dict[str, str])  # => empty unless a header is needed
    body: dict[str, object] = field(default_factory=dict[str, object])  # => the resource or error payload


def list_articles_v1(after_cursor: str | None, limit: int) -> Response:  # => co-17: GET /v1/articles
    all_ids = sorted(STORE.keys())  # => co-17: a stable, deterministic order to paginate over
    start = 0 if after_cursor is None else all_ids.index(int(after_cursor)) + 1  # => co-17: resumes after cursor
    page_ids = all_ids[start : start + limit]  # => co-17: exactly `limit` ids, or fewer at the end
    edges = [{"node": STORE[i], "cursor": str(i)} for i in page_ids]  # => co-17: openapi.yaml's own envelope
    has_next = (start + limit) < len(all_ids)  # => co-17: are there more items after this page?
    end_cursor = edges[-1]["cursor"] if edges else None  # => co-17: the cursor the NEXT request resumes from
    body: dict[str, object] = {"edges": edges, "pageInfo": {"hasNextPage": has_next, "endCursor": end_cursor}}
    return Response(status=200, body=body)  # => co-09: matches openapi.yaml's declared 200 schema


def create_article_v1(idempotency_key: str, title: str) -> Response:  # => co-18: POST /v1/articles
    if idempotency_key in IDEMPOTENCY_STORE:  # => co-18: a REPLAY -- do NOT create a second article
        return Response(status=200, body=IDEMPOTENCY_STORE[idempotency_key])  # => co-18: the ORIGINAL response
    new_id = NEXT_ID[0]  # => a fresh id for a genuinely new article
    article: dict[str, object] = {"id": new_id, "title": title}  # => co-09: matches openapi.yaml's Article
    STORE[new_id] = article  # => co-09: writes into the SAME store list_articles_v1 reads from
    IDEMPOTENCY_STORE[idempotency_key] = article  # => co-18: recorded so a FUTURE replay of this key is safe
    NEXT_ID[0] += 1  # => advances the counter for the NEXT genuinely new article
    return Response(status=201, body=article)  # => co-09: matches openapi.yaml's declared 201 schema


def get_article_v1(article_id: int) -> Response:  # => co-30: GET /v1/articles/{id}
    if article_id not in STORE:  # => the requested resource does not exist
        problem: dict[str, object] = {  # => co-30: RFC 9457's application/problem+json envelope
            "type": "https://example.com/probs/not-found",  # => a URI identifying this problem TYPE
            "title": "Article Not Found",  # => a short, human-readable summary
            "status": 404,  # => co-30: the SAME status, echoed inside the body too
            "detail": f"No article with id {article_id}",  # => specific to THIS occurrence
        }  # => end of the problem+json body
        return Response(status=404, body=problem)  # => co-09: matches openapi.yaml's declared 404 schema
    return Response(status=200, body=STORE[article_id])  # => 200, the found resource


charge_count_before_replay = len(STORE)  # => co-18: the store's size BEFORE any replay is attempted

first_write = create_article_v1("cap-key-1", "Capstone Article")  # => a genuinely new idempotency key
print(f"first write: status={first_write.status}, body={first_write.body}")  # => Output: 201, new article

replayed_write = create_article_v1("cap-key-1", "Capstone Article")  # => co-18: resends the SAME key
print(f"replayed write: status={replayed_write.status}, body={replayed_write.body}")  # => Output: 200, IDENTICAL

did_not_double_apply = len(STORE) == charge_count_before_replay + 1  # => co-18: exactly ONE new article total
print(f"replay did not double-apply: {did_not_double_apply}")  # => Output: True

page = list_articles_v1(after_cursor=None, limit=10)  # => confirms the write is now visible via GET
print(f"list after write: status={page.status}, {page.body}")  # => Output: 200, both articles present

missing = get_article_v1(999)  # => co-30: a request for a resource that never existed
print(f"missing article: status={missing.status}, {missing.body['title']}")  # => Output: 404, Article Not Found
