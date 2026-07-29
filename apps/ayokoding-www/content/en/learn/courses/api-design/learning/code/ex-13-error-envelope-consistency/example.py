# pyright: strict
"""Example 13: The Same Error Shape Across Three Endpoints. (co-30)

An API is a promise: every endpoint's error looks the same SHAPE, so one
client-side error handler works everywhere. This example runs the identical
`build_problem()` helper for three DIFFERENT failures and confirms all three
bodies share the same top-level key set.
"""

from dataclasses import dataclass, asdict  # => asdict: turns each record into a comparable dict


@dataclass  # => co-30: one shape, reused for every failure below
class ProblemDetails:  # => co-30: five fields, identical for every endpoint in this file
    type: str  # => the stable problem category URI
    title: str  # => a short, human summary of that category
    status: int  # => the HTTP status, repeated inside the body
    detail: str  # => this occurrence's own explanation
    instance: str  # => this occurrence's own identifying URI


def build_problem(kind: str, status: int, detail: str, instance: str) -> ProblemDetails:
    # => co-30: the SINGLE function every endpoint below calls -- no bespoke shape per route
    return ProblemDetails(  # => builds one problem body from the four caller-supplied facts
        type=f"https://api.example.com/problems/{kind}",  # => derived from the failure's own kind
        title=kind.replace("-", " ").title(),  # => a readable title, derived from the same kind
        status=status,  # => whatever status code the caller passed in
        detail=detail,  # => whatever explanation the caller passed in
        instance=instance,  # => whatever instance URI the caller passed in
    )  # => end of the ProblemDetails construction


not_found = build_problem("not-found", 404, "Article 999 does not exist.", "/articles/999")  # => endpoint 1
conflict = build_problem("conflict", 409, "Username 'ada' already taken.", "/users")  # => endpoint 2
validation = build_problem("validation-error", 422, "age must be non-negative.", "/users")  # => endpoint 3
# => co-30: three UNRELATED endpoints (articles, users x2), one shared error-building function

for problem in (not_found, conflict, validation):  # => print all three side by side
    print(f"{problem.status}: keys={sorted(asdict(problem).keys())}")  # => Output: identical key list
    # => keys is always ['detail', 'instance', 'status', 'title', 'type'] -- same 5, every endpoint

key_sets = {frozenset(asdict(p).keys()) for p in (not_found, conflict, validation)}  # => a set-of-sets
# => co-30: collapsing all three key sets into a set-of-sets -- consistency means only ONE survives
print(f"distinct shapes across all three endpoints: {len(key_sets)}")  # => Output: 1
