# pyright: strict
"""Example 2: RPC-Style vs. Resource-Style URIs. (co-05)

Contrasts an RPC-flavored endpoint (`/getArticle?id=1`, a verb baked into the
path) against the resource-oriented equivalent (`GET /articles/1`, a noun in
the path with the verb carried by the HTTP method instead).
"""

import re  # => reuse the same verb-detection idea as Example 1

VERB_PATTERN = re.compile(r"\b(get|list|create|delete|update|fetch)\b", re.IGNORECASE)
# => a compiled regex flagging any verb word left in a URI's path segment


def classify(method: str, path: str) -> str:  # => labels one (method, path) pair
    has_verb_in_path = VERB_PATTERN.search(path) is not None  # => True: a verb leaked into the path
    # => True means the path itself smuggled an action word into what should be a noun
    return "RPC-style (verb in path)" if has_verb_in_path else "resource-style (noun in path)"
    # => co-05: the method already carries the verb, so a verb-free path is what "wins"


# The SAME intent -- "read article 1" -- expressed two different ways.
RPC_STYLE = ("GET", "/getArticle?id=1")  # => the verb "get" is baked into the PATH itself
# => RPC_STYLE is ("GET", "/getArticle?id=1") (type: tuple[str, str])
RESOURCE_STYLE = ("GET", "/articles/1")  # => the path is a pure noun; GET alone carries the verb
# => RESOURCE_STYLE is ("GET", "/articles/1") (type: tuple[str, str])

for method, path in (RPC_STYLE, RESOURCE_STYLE):  # => run the classifier over both forms
    label = classify(method, path)  # => co-05: resource-style is verb-free, RPC-style is not
    # => label is "RPC-style (verb in path)" on the first pass, "resource-style (noun in path)" on the second
    print(f"{method} {path!r} -> {label}")  # => Output: two lines, contrasting labels
