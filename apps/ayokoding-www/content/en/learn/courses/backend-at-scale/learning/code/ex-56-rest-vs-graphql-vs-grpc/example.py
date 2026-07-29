# pyright: strict
"""Example 56: REST vs GraphQL vs gRPC -- the same operation three ways. (co-07, co-08)

The SAME fetch (get an article's title) expressed three ways: a fixed-shape
REST JSON response, a caller-shaped GraphQL field selection, and a typed gRPC
unary RPC. Each works; the printed note names when each style fits.
"""

from dataclasses import dataclass  # => a small typed record for the gRPC message
from typing import Any  # => GraphQL/REST responses are arbitrary nested JSON

RECORD: dict[str, object] = {"id": 1, "title": "Same data, three styles", "body": "..."}  # => the single source of truth


def rest_fetch() -> dict[str, object]:  # => co-07: REST -- a fixed-shape JSON response (cacheable via GET)
    return RECORD  # => returns every field


def graphql_fetch(requested: list[str]) -> dict[str, Any]:  # => co-07: GraphQL -- the caller picks fields (no over-fetch)
    return {field: RECORD[field] for field in requested if field in RECORD}  # => caller-shaped


@dataclass  # => co-08: a typed protobuf-like message
class ArticleRequest:
    article_id: int  # => the id to fetch


@dataclass  # => co-08: a typed protobuf-like response
class ArticleResponse:
    title: str  # => a single typed field


def grpc_fetch(request: ArticleRequest) -> ArticleResponse:  # => co-08: gRPC -- a typed unary RPC over HTTP/2
    return ArticleResponse(title=str(RECORD["title"]))  # => a typed response (binary on the wire in real gRPC)


rest = rest_fetch()  # => co-07: works -- best for public, cacheable APIs
gql = graphql_fetch(["title"])  # => co-07: works -- best when callers need different shapes
rpc = grpc_fetch(ArticleRequest(1))  # => co-08: works -- best for typed internal service-to-service calls
print(f"REST title:     {rest['title']}")  # => Output: Same data, three styles
print(f"GraphQL title:  {gql['title']}")  # => Output: Same data, three styles
print(f"gRPC title:     {rpc.title}")  # => Output: Same data, three styles
print("each fits: REST=cacheable/public, GraphQL=caller-shaped, gRPC=typed/internal")  # => Output: when each wins

assert rest["title"] == gql["title"] == rpc.title  # => co-07/co-08: the same data, three working styles
