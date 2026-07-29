# pyright: strict
"""Example 56: A HAL Response with _links and _embedded. (co-28)

HAL (`application/hal+json`) is a concrete hypermedia format: `_links` is
REQUIRED (co-28's own mechanism from Example 11, standardized), `_embedded`
is optional -- inline sub-resources instead of a second round trip.
"""

from typing import Any  # => a HAL document is arbitrary nested JSON


def hal_article(article_id: int, title: str, author_id: int, author_name: str) -> dict[str, Any]:
    # => GET /articles/{id} -- co-28: builds a HAL-shaped response
    article_links = {  # => co-28: REQUIRED in HAL -- at minimum, a "self" link
        "self": {"href": f"/articles/{article_id}"},  # => co-28: where THIS resource lives
        "author": {"href": f"/authors/{author_id}"},  # => co-28: a link to a RELATED resource
    }  # => end of article_links
    embedded_author = {  # => the author's OWN mini-representation, embedded directly
        "id": author_id,  # => the author's own id
        "name": author_name,  # => the author's own name
        "_links": {"self": {"href": f"/authors/{author_id}"}},  # => HAL nests recursively
    }  # => end of embedded_author
    return {  # => co-28: the standardized HAL envelope
        "id": article_id,  # => the resource's own plain attributes
        "title": title,  # => another plain attribute
        "_links": article_links,  # => co-28: REQUIRED -- at least a "self" link
        "_embedded": {"author": embedded_author},  # => co-28: OPTIONAL -- inlines instead of a 2nd GET
    }  # => end of the hal_article construction


response = hal_article(1, "Hello, API Design", 7, "Ada")  # => build one HAL response
print(f"_links: {response['_links']}")  # => Output: self + author links
print(f"_embedded author: {response['_embedded']['author']}")  # => Output: the inlined author record
# => a client can render the author WITHOUT a second GET /authors/7 round trip
