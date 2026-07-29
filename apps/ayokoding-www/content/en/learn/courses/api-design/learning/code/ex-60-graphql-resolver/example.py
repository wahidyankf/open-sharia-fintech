# pyright: strict
"""Example 60: A Resolver Resolving a Field. (co-25)

A resolver is a small function bound to ONE field -- when the executor
(Example 58) needs that field's value, it calls the field's own resolver
rather than reading a fixed dictionary directly, letting a field's value be
computed instead of merely stored.
"""

from typing import Callable  # => a resolver is just a function, typed for clarity

ARTICLES: dict[str, dict[str, object]] = {"1": {"id": "1", "title": "Hello", "view_count": 42}}
# => co-25: the underlying store a resolver reads from


def resolve_title(article_id: str) -> str:  # => co-25: a resolver for the "title" field specifically
    return str(ARTICLES[article_id]["title"])  # => co-25: reads the stored value directly


def resolve_view_count_doubled(article_id: str) -> int:  # => co-25: a resolver that COMPUTES its value
    raw_value = ARTICLES[article_id]["view_count"]  # => co-25: the raw stored value, typed as object
    assert isinstance(raw_value, int)  # => co-25: narrows object -> int before arithmetic, pyright-clean
    return raw_value * 2  # => co-25: the field's VALUE is derived, not merely stored verbatim


FIELD_RESOLVERS: dict[str, Callable[[str], object]] = {  # => co-25: field name -> its own resolver function
    "title": resolve_title,  # => a simple pass-through resolver
    "view_count_doubled": resolve_view_count_doubled,  # => a resolver that computes its own value
}  # => end of FIELD_RESOLVERS


def resolve_field(field_name: str, article_id: str) -> object:  # => co-25: the executor's own dispatch step
    resolver = FIELD_RESOLVERS[field_name]  # => co-25: looks up the specific field's resolver
    return resolver(article_id)  # => co-25: calls it -- the field's value is whatever the function returns


title_value = resolve_field("title", "1")  # => co-25: resolves a plain, stored field
print(f"title: {title_value}")  # => Output: title: Hello

doubled_value = resolve_field("view_count_doubled", "1")  # => co-25: resolves a COMPUTED field
# => doubled_value is 84 (type: object, runtime type int) -- never stored anywhere, only computed
print(f"view_count_doubled: {doubled_value}")  # => Output: view_count_doubled: 84 -- 42 doubled
