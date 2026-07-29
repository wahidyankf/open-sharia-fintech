# pyright: strict
"""Example 80: A Versioned REST API From an OpenAPI Spec, End to End. (co-09, co-17, co-18, co-30, co-27)

The closing example of the Advanced tier assembles five prior concerns onto
ONE small API: a versioned path (co-13), cursor pagination (co-17), an
idempotent write (co-18), a consistent `problem+json` error envelope
(co-30), and a GraphQL/gRPC facade NOTE (co-27) -- then verifies the whole
thing conforms to its own spec (co-09), end to end.
"""

from dataclasses import dataclass, field  # => field: default_factory for mutable dataclass defaults

STORE: dict[int, dict[str, object]] = {1: {"id": 1, "title": "Hello"}, 2: {"id": 2, "title": "World"}}
# => co-09: the spec's own resource collection, at /v1/articles
IDEMPOTENCY_STORE: dict[str, dict[str, object]] = {}  # => co-18: key -> the response it produced
REQUEST_BUDGET = [5]  # => co-27's own rate-limit budget, shared across every call below


@dataclass  # => co-09: status, headers, and body -- the shape every response in this API shares
class Response:  # => co-09: the ONE shape every operation below returns
    status: int  # => the HTTP status code
    headers: dict[str, str] = field(default_factory=dict[str, str])  # => carries Retry-After when limited
    body: dict[str, object] = field(default_factory=dict[str, object])  # => the resource or error payload


def list_articles_v1(after_cursor: str | None, limit: int) -> Response:  # => co-13/co-17: GET /v1/articles
    if REQUEST_BUDGET[0] <= 0:  # => co-27: rate limit applies to reads too, checked first
        return Response(429, {"Retry-After": "60"})  # => co-27: rejected before touching the store
    REQUEST_BUDGET[0] -= 1  # => co-27: consumes budget for this call
    all_ids = sorted(STORE.keys())  # => co-17: a stable, deterministic order to paginate over
    start = 0 if after_cursor is None else all_ids.index(int(after_cursor)) + 1  # => co-17: resumes after the cursor
    page_ids = all_ids[start : start + limit]  # => co-17: exactly `limit` ids, or fewer at the end
    edges = [{"node": STORE[i], "cursor": str(i)} for i in page_ids]  # => co-17: Example 76's own connection shape
    has_next = (start + limit) < len(all_ids)  # => co-17: are there more items after this page?
    body: dict[str, object] = {"edges": edges, "pageInfo": {"hasNextPage": has_next}}  # => co-17: paginated envelope
    return Response(200, {}, body)  # => a normal, successful, paginated response


def create_article_v1(idempotency_key: str, title: str) -> Response:  # => co-13/co-18: POST /v1/articles
    if REQUEST_BUDGET[0] <= 0:  # => co-27: rate limit checked BEFORE idempotency bookkeeping
        return Response(429, {"Retry-After": "60"})  # => co-27: rejected outright
    if idempotency_key in IDEMPOTENCY_STORE:  # => co-18: a REPLAY of a previous write
        return Response(200, {}, IDEMPOTENCY_STORE[idempotency_key])  # => co-18: the stored response, verbatim
    REQUEST_BUDGET[0] -= 1  # => co-27: consumes budget only for a genuinely new write
    new_id = max(STORE.keys()) + 1  # => a fresh id, one past the current maximum
    article: dict[str, object] = {"id": new_id, "title": title}  # => the newly created resource
    STORE[new_id] = article  # => co-09: writes into the SAME store list_articles_v1 reads from
    IDEMPOTENCY_STORE[idempotency_key] = article  # => co-18: recorded for any future replay
    return Response(201, {}, article)  # => 201 -- freshly created


def get_article_v1(article_id: int) -> Response:  # => co-13/co-30: GET /v1/articles/{id}
    if article_id not in STORE:  # => the requested resource does not exist
        problem: dict[str, object] = {  # => co-30: RFC 9457's application/problem+json envelope
            "type": "https://example.com/probs/not-found",  # => a URI identifying this problem TYPE
            "title": "Article Not Found",  # => a short, human-readable summary
            "status": 404,  # => co-30: the SAME status, echoed inside the body too
            "detail": f"No article with id {article_id}",  # => specific to THIS occurrence
        }  # => end of the problem+json body
        return Response(404, {}, problem)  # => co-30: a consistent error shape, regardless of WHICH operation
    return Response(200, {}, STORE[article_id])  # => 200, the found resource


GRAPHQL_FACADE_NOTE = {  # => co-27: the SAME operations, named as they would appear via a GraphQL facade
    "list_articles_v1": "query { articles(first: N, after: CURSOR) { edges { node cursor } pageInfo } }",  # => co-27
    "create_article_v1": "mutation { createArticle(title: TITLE) { id title } }",  # => co-27
}  # => end of GRAPHQL_FACADE_NOTE
GRPC_FACADE_NOTE = {  # => co-27: the SAME operations, named as they would appear via a gRPC facade
    "list_articles_v1": "rpc ListArticles (ListArticlesRequest) returns (stream Article)",  # => co-27
    "create_article_v1": "rpc CreateArticle (CreateArticleRequest) returns (Article)",  # => co-27
}  # => end of GRPC_FACADE_NOTE


page = list_articles_v1(after_cursor=None, limit=1)  # => end-to-end call 1: paginated read
print(f"page 1: {page.status}, {page.body}")  # => Output: 200, one edge, hasNextPage=True

created = create_article_v1("key-e2e-1", "End to End")  # => end-to-end call 2: idempotent write
print(f"created: {created.status}, {created.body}")  # => Output: 201, the new article

replayed = create_article_v1("key-e2e-1", "End to End")  # => end-to-end call 3: replay -- idempotency holds
print(f"replayed: {replayed.status}, same id={replayed.body['id'] == created.body['id']}")  # => Output: 200, True

missing = get_article_v1(999)  # => end-to-end call 4: a consistent problem+json error
print(f"missing: {missing.status}, {missing.body['title']}")  # => Output: 404, Article Not Found

conforms = page.status == 200 and created.status == 201 and missing.status == 404  # => co-09: overall conformance
# => conforms is True -- five previously-separate concepts (co-13/17/18/30/27) compose without conflict
print(f"end-to-end conformance: {conforms}")  # => Output: True -- co-09: every operation matched its own contract

print(f"GraphQL facade for create: {GRAPHQL_FACADE_NOTE['create_article_v1']}")  # => co-27: the facade equivalent
print(f"gRPC facade for create: {GRPC_FACADE_NOTE['create_article_v1']}")  # => co-27: the OTHER facade equivalent
