# pyright: strict
"""Example 32: Adding an Optional Field Is Backward-Compatible. (co-14)

Adding a NEW, optional field to a response never breaks an existing client
that only reads the fields it already knew about -- this is the single most
common, safest way an API evolves without a version bump.
"""

from dataclasses import dataclass  # => a small typed response record for this example


@dataclass  # => co-14: the CURRENT shape a v1 client was written against
class ArticleV1:
    id: int  # => the article's own id
    title: str  # => the article's own title


def get_article_v1() -> ArticleV1:  # => the ORIGINAL handler, unchanged
    return ArticleV1(id=1, title="Hello")  # => the shape a v1 client already expects


def get_article_evolved() -> dict[str, object]:  # => co-14: the SAME endpoint, now with one MORE field
    return {"id": 1, "title": "Hello", "author": "Ada"}  # => co-14: additive -- nothing removed or renamed


def old_client_reads(response: dict[str, object]) -> ArticleV1:  # => co-14: reads ONLY id/title, like before
    return ArticleV1(id=response["id"], title=response["title"])  # type: ignore[arg-type]  # => old fields only


original = get_article_v1()  # => the shape before the change
print(f"before: {original}")  # => Output: ArticleV1(id=1, title='Hello')

evolved_response = get_article_evolved()  # => the SAME endpoint, after adding "author"
# => evolved_response has 3 keys now, but old_client_reads only ever looks at 2 of them
old_view = old_client_reads(evolved_response)  # => co-14: an old client, unaware "author" now exists
print(f"old client still works: {old_view}")  # => Output: ArticleV1(id=1, title='Hello') -- unaffected
