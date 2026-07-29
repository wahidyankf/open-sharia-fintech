# pyright: strict
"""Example 65: A Server-Streaming RPC. (co-26)

Unlike Example 64's one-request-one-response unary call, a server-streaming
RPC takes ONE request but returns MANY response messages over time -- a
Python generator models this naturally: the client makes one call, then
iterates over a stream of results.
"""

from collections.abc import Iterator  # => co-26: the streaming response is an Iterator, not a single value
from dataclasses import dataclass  # => typed request/response messages

ARTICLES_BY_AUTHOR = {"a1": ["Hello", "World", "gRPC Streaming"]}  # => co-26: multiple titles per author


@dataclass  # => co-26: ONE request message, naming which author's articles to stream
class ListArticlesRequest:  # => co-26: exactly one field, matching the .proto request shape
    author_id: str  # => the single field the request carries


@dataclass  # => co-26: each individually-streamed response message
class ArticleTitle:  # => co-26: exactly one field per streamed message
    title: str  # => one title per streamed message


def list_articles_by_author(request: ListArticlesRequest) -> Iterator[ArticleTitle]:  # => co-26: server-streaming
    titles = ARTICLES_BY_AUTHOR[request.author_id]  # => co-26: ONE request resolves the WHOLE list up front
    for title in titles:  # => co-26: but the RESPONSE is yielded one message at a time
        yield ArticleTitle(title=title)  # => co-26: each yield is a separate streamed response message


request = ListArticlesRequest(author_id="a1")  # => the single request that starts the stream
streamed_titles = list(list_articles_by_author(request))  # => co-26: consumes the FULL stream into a list
# => streamed_titles has 3 ArticleTitle entries -- one request produced three response messages
print(f"streamed {len(streamed_titles)} messages: {streamed_titles}")  # => Output: 3 ArticleTitle messages

for i, article_title in enumerate(list_articles_by_author(request), start=1):  # => co-26: iterate lazily too
    print(f"message {i}: {article_title.title}")  # => Output: one line per streamed title, in order
