DEFAULT_LIMIT = 10  # => co-19: list endpoints page results with a DEFAULTED limit
MAX_LIMIT = 100  # => co-19: and a BOUNDED limit -- callers can't demand the whole table at once


def parse_pagination(params: dict[str, str]) -> tuple[int, int]:  # => returns (limit, offset)
    raw_limit = params.get("limit")  # => absent when the caller sends no ?limit= at all
    raw_offset = params.get("offset")  # => absent when the caller sends no ?offset= at all

    limit = int(raw_limit) if raw_limit is not None else DEFAULT_LIMIT  # => fall back to the default
    offset = int(raw_offset) if raw_offset is not None else 0  # => a page always starts at 0 by default

    if limit < 0 or offset < 0:  # => negative values make no sense as a window into a list
        raise ValueError("limit and offset must be non-negative")
    limit = min(limit, MAX_LIMIT)  # => co-19: clamp an over-large request instead of scanning everything

    return limit, offset


defaults = parse_pagination({})  # => neither param supplied
explicit = parse_pagination({"limit": "25", "offset": "50"})  # => a normal page request
clamped = parse_pagination({"limit": "9999", "offset": "0"})  # => an abusive over-large limit

print(defaults)  # => Output: (10, 0)
print(explicit)  # => Output: (25, 50)
print(clamped)  # => Output: (100, 0) -- clamped down to MAX_LIMIT, never trusted as-is

assert defaults == (10, 0)
assert explicit == (25, 50)
assert clamped == (100, 0)

try:
    parse_pagination({"limit": "-5"})  # => a negative limit is rejected outright
    raised = False
except ValueError:
    raised = True
print(raised)  # => Output: True
assert raised is True
print("kata-04 OK")
