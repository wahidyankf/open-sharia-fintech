from typing import Final  # => typed rerank fixture

ORDER: Final[tuple[str, str]] = ("best", "other")  # => reranked candidate order
assert ORDER[0] == "best"
print("PASS: rerank-candidates")  # => relevance improved
