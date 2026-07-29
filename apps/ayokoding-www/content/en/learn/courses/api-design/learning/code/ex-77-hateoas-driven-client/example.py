# pyright: strict
"""Example 77: A Client That Follows Links Instead of Hardcoded URLs. (co-28)

A HATEOAS-driven client never hardcodes `/authors/{id}` -- it starts at ONE
known root URL, then NAVIGATES purely by reading `_links` out of each HAL
response (Example 56), the way a human clicks links in a browser instead of
typing every URL from memory.
"""

from typing import Any  # => the HAL responses are arbitrary nested JSON

SERVER: dict[str, dict[str, Any]] = {  # => co-28: a tiny in-memory "server" -- URL -> its own HAL response
    "/": {"_links": {"articles": {"href": "/articles/1"}}},  # => co-28: the ONLY hardcoded URL a client needs
    "/articles/1": {  # => an article resource, reached ONLY by following a link
        "id": 1,  # => the article's own plain attribute
        "title": "Hello, API Design",  # => another plain attribute
        "_links": {"self": {"href": "/articles/1"}, "author": {"href": "/authors/7"}},  # => co-28: more links
    },  # => end of the /articles/1 entry
    "/authors/7": {"id": 7, "name": "Ada", "_links": {"self": {"href": "/authors/7"}}},  # => the final resource
}  # => end of SERVER

ROOT_URL = "/"  # => co-28: the ONE URL this client is allowed to hardcode


def follow_link(current_response: dict[str, Any], relation: str) -> dict[str, Any]:  # => co-28: navigation step
    target_href = current_response["_links"][relation]["href"]  # => co-28: reads the URL FROM the response
    return SERVER[target_href]  # => co-28: "fetches" it -- the client never constructed this URL itself


visited_urls: list[str] = []  # => records every URL actually visited, to prove no hardcoding beyond ROOT_URL

root_response = SERVER[ROOT_URL]  # => co-28: step 1 -- the ONLY hardcoded fetch
visited_urls.append(ROOT_URL)  # => records the root visit

article_response = follow_link(root_response, "articles")  # => co-28: step 2 -- follows the "articles" link
visited_urls.append(article_response["_links"]["self"]["href"])  # => records the article's own self-link

author_response = follow_link(article_response, "author")  # => co-28: step 3 -- follows the "author" link
visited_urls.append(author_response["_links"]["self"]["href"])  # => records the author's own self-link

print(f"visited: {visited_urls}")  # => Output: ['/', '/articles/1', '/authors/7'] -- discovered, not hardcoded
print(f"final resource: {author_response}")  # => Output: the author record, reached via two link hops
# => the client's ONLY string literal was ROOT_URL -- every other URL came from a prior response
