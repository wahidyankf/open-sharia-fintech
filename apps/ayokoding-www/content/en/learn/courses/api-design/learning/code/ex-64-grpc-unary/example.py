# pyright: strict
"""Example 64: A Unary RPC. (co-26)

A unary RPC is the gRPC shape closest to a normal function call -- ONE
request message in, ONE response message out, matching Example 63's
`GetArticle` service definition, simulated here as a plain in-process
call rather than an actual network round trip.
"""

from dataclasses import dataclass  # => typed request/response messages, matching the .proto shapes

ARTICLES = {"1": "Hello, gRPC"}  # => co-26: the underlying store the RPC handler reads from


@dataclass  # => co-26: mirrors PROTO_SOURCE's ArticleRequest message
class ArticleRequest:  # => co-26: exactly one field, matching the .proto message
    id: str  # => the single field the request message carries


@dataclass  # => co-26: mirrors PROTO_SOURCE's ArticleResponse message
class ArticleResponse:  # => co-26: exactly two fields, matching the .proto message
    id: str  # => echoes the requested id back
    title: str  # => the resolved title


def get_article(request: ArticleRequest) -> ArticleResponse:  # => co-26: the unary RPC handler itself
    title = ARTICLES[request.id]  # => co-26: ONE request in -> a lookup against the store
    return ArticleResponse(id=request.id, title=title)  # => co-26: ONE response out -- unary, start to finish


request = ArticleRequest(id="1")  # => the single request message a client sends
response = get_article(request)  # => co-26: the unary call -- one request, one response, nothing streamed
# => response is ArticleResponse(id='1', title='Hello, gRPC') -- exactly the shape .proto declared
print(f"response: {response}")  # => Output: ArticleResponse(id='1', title='Hello, gRPC')
