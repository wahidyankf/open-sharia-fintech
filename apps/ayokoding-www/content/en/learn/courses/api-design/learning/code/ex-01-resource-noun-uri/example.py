# pyright: strict
"""Example 1: Resource-Noun URIs. (co-05)

A resource URI names a NOUN -- a collection or a single item -- never a verb.
This is the first move of resource modeling: decide what THING the URI
identifies, then let HTTP methods (Example 3) carry the ACTION separately.
"""

import re  # => stdlib only, no third-party dependency needed for this check
# => re.compile below builds a reusable pattern, not a fresh one per call

# A collection URI (plural noun) and an item URI (collection + identifier).
COLLECTION_URI = "/articles"  # => co-05: a plural noun names the whole set
# => COLLECTION_URI is "/articles" (type: str)
ITEM_URI = "/articles/42"  # => co-05: the SAME noun, narrowed to one member by id
# => ITEM_URI is "/articles/42" (type: str) -- same noun, one extra path segment

# A verb anywhere in a path segment is the one smell resource-naming forbids --
# words like "get", "create", "list", "delete" describe an ACTION, not a THING.
VERB_PATTERN = re.compile(r"\b(get|list|create|delete|update|fetch)\b", re.IGNORECASE)
# => a compiled regex, reused for both checks below (co-05's naming rule)
# => IGNORECASE means "Get" and "GET" are caught too, not just lowercase "get"


def is_noun_uri(uri: str) -> bool:  # => True when no verb word appears in the path
    return VERB_PATTERN.search(uri) is None  # => False the moment a verb word is found


for uri in (COLLECTION_URI, ITEM_URI):  # => check BOTH the collection and item forms
    verdict = "noun-based (OK)" if is_noun_uri(uri) else "verb-based (BAD)"  # => co-05's own verdict
    # => verdict is always "noun-based (OK)" here since neither URI contains a verb word
    print(f"{uri!r} -> {verdict}")  # => Output: one line per URI, both should read "noun-based"
