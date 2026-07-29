# pyright: strict
"""Example 12: The application/problem+json Error Envelope. (co-08)

RFC 9457 defines a standard error shape -- `type`, `title`, `status`,
`detail`, `instance` -- served as `application/problem+json`. This example
builds one such body for a 404 and prints it as JSON.
"""

import json  # => stdlib: turns the dict into the actual wire format
from dataclasses import dataclass, asdict  # => asdict: converts the record into a plain dict


@dataclass  # => co-08: the five RFC 9457 fields, one dataclass field each
class ProblemDetails:
    type: str  # => a URI identifying the PROBLEM TYPE (a stable, dereferenceable category)
    title: str  # => a short, human-readable summary of the problem type
    status: int  # => the HTTP status code, repeated here for a client reading only the body
    detail: str  # => a human-readable explanation specific to THIS occurrence
    instance: str  # => a URI identifying THIS specific occurrence of the problem


def not_found_problem(article_id: int) -> ProblemDetails:  # => builds a 404 problem body
    return ProblemDetails(  # => co-08: all five fields populated -- no field left implicit
        type="https://api.example.com/problems/not-found",  # => the stable problem category
        title="Resource Not Found",  # => a short, human summary of that category
        status=404,  # => repeats the HTTP status inside the body itself
        detail=f"Article {article_id} does not exist.",  # => THIS occurrence's own explanation
        instance=f"/articles/{article_id}",  # => THIS occurrence's own identifying URI
    )  # => end of the ProblemDetails construction


problem = not_found_problem(999)  # => build one problem body for a missing article
# => problem.type is "https://api.example.com/problems/not-found" (type: str)
body_json = json.dumps(asdict(problem), indent=2)  # => co-08: the actual application/problem+json body
# => body_json is a str: pretty-printed JSON with exactly the five RFC 9457 keys
print(body_json)  # => Output: a 5-key JSON object, matching RFC 9457's fields exactly
